from ai.preprocessing import process_ai_output


def test_ai_filtering_and_priority():

    bins = [
        {"level": 10},   # rejet
        {"level": 45},   # normal
        {"level": 75},   # prioritaire
        {"level": 95}    # urgent
    ]

    processed = process_ai_output(bins)

    # 10% doit être supprimé
    assert len(processed) == 3

    # Vérifie présence des time windows
    for b in processed:
        assert "time_window" in b