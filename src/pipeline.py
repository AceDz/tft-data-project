from src.config import GAME_NAME, TAG_LINE, MATCH_COUNT
from src.extract import get_puuid, get_match_ids, get_match
from src.storage import save_raw_match


def run_pipeline():
    print("🚀 Starting TFT ingestion pipeline")

    # 1. Get PUUID
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    print("✅ PUUID obtained")

    # 2. Get matches
    match_ids = get_match_ids(puuid, MATCH_COUNT)
    print(f"📦 {len(match_ids)} matches found")

    # 3. Download + save raw
    for match_id in match_ids:

        match_data = get_match(match_id)

        if match_data is None:
            print(f"❌ Failed match {match_id}")
            continue

        path = save_raw_match(match_id, match_data)

        print(f"💾 Saved {match_id} → {path}")

    print("🎉 Pipeline finished")


if __name__ == "__main__":
    run_pipeline()