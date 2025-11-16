#!/usr/bin/env python
"""
Simple analytics helper for the RF site SQLite database.

Usage examples:

    # Show a quick summary of events & pageviews by variant
    python analytics_cli.py summary

    # Show events by variant for a specific event name
    python analytics_cli.py events --event click_buy-now_hero

    # Show pageviews by variant for a given page
    python analytics_cli.py pageviews --page /

    # Show conversion (events/pageviews) per variant
    python analytics_cli.py conversion --event click_buy-now_hero --page /

    # Show conversion (events/user) per variant
    python analytics_cli.py events-detailed --event click_buy-now_hero

    # Show events for a family of names (using SQL LIKE)
    python analytics_cli.py events-like --pattern 'click_buy-now_%'

You can override the DB path with --db or RF_SITE_DB env var.
"""

import os
import sqlite3
import argparse
from typing import Dict, Any, Tuple, Optional

DB_URL = "/app/data/rf_site.db"
# DB_URL = "/app/rf_site.db"  # DEBUG ONLY


# --------- helpers for nice display --------- #

def parse_event_name_components(event_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Very small parser for display only.

    Expected pattern: <action>_<target>_<location>
    Example: click_buy-now_hero

    Returns (action, target, location), or (None, None, None) if it doesn't fit.
    """
    parts = event_name.split("_", 2)
    if len(parts) == 3:
        return parts[0], parts[1], parts[2]
    return None, None, None


def maybe_print_event_context(event_name: str, indent: str = "") -> None:
    """
    Prints a human-friendly interpretation of the event name if it matches the pattern.
    """
    action, target, location = parse_event_name_components(event_name)
    if action and target and location:
        print(
            f"{indent}Event breakdown → "
            f"action='{action}', target='{target}', location='{location}'"
        )


# --------- DB connection --------- #

def get_connection(db_path: str) -> sqlite3.Connection:
    if not os.path.exists(db_path):
        raise SystemExit(f"[ERROR] Database file not found: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


# --------- analytics queries --------- #

def events_detailed_by_variant(conn: sqlite3.Connection, event_name: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            variant_name,
            COUNT(*) AS total_events,
            COUNT(DISTINCT session_id) AS unique_sessions
        FROM events
        WHERE event_name = ?
        GROUP BY variant_name
        ORDER BY variant_name
        """,
        (event_name,),
    )
    rows = cur.fetchall()
    if not rows:
        print(f"No events found for event_name='{event_name}'")
        return

    print(f"\nDetailed stats for event '{event_name}' by variant:")
    maybe_print_event_context(event_name, indent="  ")
    print("-" * 70)
    print(f"{'Variant':<10} {'Total':>10} {'Unique':>10} {'Avg per session':>18}")
    print("-" * 70)
    for r in rows:
        total = r["total_events"]
        unique = r["unique_sessions"]
        avg = total / unique if unique else 0.0
        print(f"{r['variant_name']:<10} {total:>10} {unique:>10} {avg:>18.2f}")
    print()


def events_by_variant(conn: sqlite3.Connection, event_name: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT variant_name, COUNT(*) AS count
        FROM events
        WHERE event_name = ?
        GROUP BY variant_name
        ORDER BY variant_name
        """,
        (event_name,),
    )
    rows = cur.fetchall()
    if not rows:
        print(f"No events found for event_name='{event_name}'")
        return
    print(f"\nEvents for '{event_name}' by variant:")
    maybe_print_event_context(event_name, indent="  ")
    print("-" * 40)
    for r in rows:
        print(f"{r['variant_name']:<10} {r['count']:>8}")
    print()


def events_like(conn: sqlite3.Connection, pattern: str):
    """Show event counts by variant for all events whose name matches a SQL LIKE pattern.

    This does *not* affect stored data; it only parses for display if the
    event names happen to follow the <action>_<target>_<location> pattern.
    """
    cur = conn.cursor()
    cur.execute(
        """
        SELECT variant_name, event_name, COUNT(*) AS count
        FROM events
        WHERE event_name LIKE ?
        GROUP BY variant_name, event_name
        ORDER BY variant_name, event_name
        """,
        (pattern,),
    )
    rows = cur.fetchall()
    if not rows:
        print(f"No events found for pattern LIKE '{pattern}'")
        return

    print(f"\nEvents matching pattern '{pattern}' by variant and name:")
    print("-" * 70)
    last_variant = None
    for r in rows:
        v = r["variant_name"]
        if v != last_variant:
            # header per variant
            print(f"\nVariant: {v}")
            print(f"  {'Action':<10} {'Target':<22} {'Location':<18} {'Count':>8}")
            print(f"  {'-'*10} {'-'*22} {'-'*18} {'-'*8}")
            last_variant = v

        event_name = r["event_name"]
        action, target, location = parse_event_name_components(event_name)
        count = r["count"]

        if action and target and location:
            print(f"  {action:<10} {target:<22} {location:<18} {count:>8}")
        else:
            # fallback for legacy/irregular names
            print(f"  {event_name:<52} {count:>8}")
    print()


def pageviews_by_variant(conn: sqlite3.Connection, page: str):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT variant_name, COUNT(*) AS count
        FROM page_views
        WHERE page = ?
        GROUP BY variant_name
        ORDER BY variant_name
        """,
        (page,),
    )
    rows = cur.fetchall()
    if not rows:
        print(f"No pageviews found for page='{page}'")
        return
    print(f"\nPageviews for '{page}' by variant:")
    print("-" * 40)
    for r in rows:
        print(f"{r['variant_name']:<10} {r['count']:>8}")
    print()


def conversion_by_variant(conn: sqlite3.Connection, event_name: str, page: str):
    cur = conn.cursor()

    # Pageviews per variant
    cur.execute(
        """
        SELECT variant_name, COUNT(*) AS pageviews
        FROM page_views
        WHERE page = ?
        GROUP BY variant_name
        """,
        (page,),
    )
    pv_rows = {r["variant_name"]: r["pageviews"] for r in cur.fetchall()}

    # Events per variant
    cur.execute(
        """
        SELECT variant_name, COUNT(*) AS events
        FROM events
        WHERE event_name = ?
          AND page_url = ?
        GROUP BY variant_name
        """,
        (event_name, page),
    )
    ev_rows = {r["variant_name"]: r["events"] for r in cur.fetchall()}

    variants = sorted(set(pv_rows.keys()) | set(ev_rows.keys()))
    if not variants:
        print(f"No data for event='{event_name}' on page='{page}'")
        return

    print(f"\nConversion for event='{event_name}' on page='{page}':")
    maybe_print_event_context(event_name, indent="  ")
    print("-" * 70)
    print(f"{'Variant':<10} {'Pageviews':>10} {'Events':>10} {'Conversion':>12}")
    print("-" * 70)
    for v in variants:
        pv = pv_rows.get(v, 0)
        ev = ev_rows.get(v, 0)
        conv = (ev / pv) if pv else 0.0
        print(f"{v:<10} {pv:>10} {ev:>10} {conv:>11.2%}")
    print()


def summary(conn: sqlite3.Connection):
    cur = conn.cursor()

    print("\n=== Events by variant and name ===")
    cur.execute(
        """
        SELECT variant_name, event_name, COUNT(*) AS count
        FROM events
        GROUP BY variant_name, event_name
        ORDER BY variant_name, event_name
        """
    )
    rows = cur.fetchall()
    if rows:
        last_variant = None
        for r in rows:
            v = r["variant_name"]
            event_name = r["event_name"]
            count = r["count"]

            action, target, location = parse_event_name_components(event_name)

            if v != last_variant:
                print(f"\nVariant: {v}")
                print(f"  {'Action':<10} {'Target':<22} {'Location':<18} {'Count':>8}")
                print(f"  {'-'*10} {'-'*22} {'-'*18} {'-'*8}")
                last_variant = v

            if action and target and location:
                print(f"  {action:<10} {target:<22} {location:<18} {count:>8}")
            else:
                # fallback for non-structured names
                print(f"  {event_name:<52} {count:>8}")
    else:
        print("No events logged yet.")

    print("\n=== Pageviews by variant and page ===")
    cur.execute(
        """
        SELECT variant_name, page, COUNT(*) AS count
        FROM page_views
        GROUP BY variant_name, page
        ORDER BY variant_name, page
        """
    )
    rows = cur.fetchall()
    if rows:
        last_variant = None
        for r in rows:
            v = r["variant_name"]
            if v != last_variant:
                print(f"\nVariant: {v}")
                last_variant = v
            print(f"  {r['page']:<20} {r['count']:>8}")
    else:
        print("No page views logged yet.")

    print()


def recent_events(conn: sqlite3.Connection, limit: int = 20):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, timestamp, variant_name, event_name, page_url, metadata
        FROM events
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (limit,),
    )
    rows = cur.fetchall()
    print(f"\nLast {len(rows)} events:")
    print("-" * 80)
    for r in rows:
        event_name = r["event_name"]
        action, target, location = parse_event_name_components(event_name)
        if action and target and location:
            extra = f" ({action}/{target}/{location})"
        else:
            extra = ""
        print(
            f"[{r['timestamp']}] {r['variant_name']:<7} "
            f"{event_name:<30}{extra:<25} {r['page_url']:<10} metadata={r['metadata']}"
        )
    print()


# --------- CLI plumbing --------- #

def parse_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description="RF site analytics CLI")

    parser.add_argument(
        "--db",
        default=os.getenv("RF_SITE_DB", DB_URL),
        help=f"Path to SQLite DB file (default: {DB_URL}, or RF_SITE_DB env var)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("summary", help="Show events and pageviews grouped by variant")

    ev = subparsers.add_parser("events", help="Show event counts by variant")
    ev.add_argument("--event", required=True, help="Event name, e.g. click_buy-now_hero")

    evd = subparsers.add_parser(
        "events-detailed", help="Show total + unique sessions by variant"
    )
    evd.add_argument("--event", required=True, help="Event name, e.g. click_buy-now_hero")

    evl = subparsers.add_parser(
        "events-like", help="Show event counts for a SQL LIKE pattern"
    )
    evl.add_argument(
        "--pattern",
        required=True,
        help="SQL LIKE pattern, e.g. 'click_buy-now_%'",
    )

    pv = subparsers.add_parser("pageviews", help="Show pageview counts by variant")
    pv.add_argument("--page", required=True, help="Page path, e.g. / or /product")

    conv = subparsers.add_parser("conversion", help="Show conversion by variant")
    conv.add_argument("--event", required=True, help="Event name, e.g. click_buy-now_hero")
    conv.add_argument("--page", required=True, help="Page path, e.g. /")

    le = subparsers.add_parser("recent", help="Show recent events")
    le.add_argument("--limit", type=int, default=20, help="How many events to show")

    return vars(parser.parse_args())


def main():
    args = parse_args()
    db_path = args.pop("db")
    command = args.pop("command")

    conn = get_connection(db_path)

    try:
        if command == "summary":
            summary(conn)
        elif command == "events":
            events_by_variant(conn, event_name=args["event"])
        elif command == "events-detailed":
            events_detailed_by_variant(conn, event_name=args["event"])
        elif command == "events-like":
            events_like(conn, pattern=args["pattern"])
        elif command == "pageviews":
            pageviews_by_variant(conn, page=args["page"])
        elif command == "conversion":
            conversion_by_variant(conn, event_name=args["event"], page=args["page"])
        elif command == "recent":
            recent_events(conn, limit=args["limit"])
    finally:
        conn.close()


if __name__ == "__main__":
    main()
