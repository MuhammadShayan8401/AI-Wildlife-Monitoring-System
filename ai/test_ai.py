from ai.stress_detection import analyze_video
from app import app

with app.app_context():
    result = analyze_video(
        "videos/tiger.mp4",
        animal_id=7,           # optional, safe if invalid
        show_video=True,        # see movement
        session_tag="March14Test"  # prevents duplicate logs
    )
    print(result)