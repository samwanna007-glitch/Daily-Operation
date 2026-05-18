# YouTube Database Schema

| Property Name | Type         | Required | Description                            |
| ------------- | ------------ | -------- | -------------------------------------- |
| Title         | Title        | Yes      | YouTube video title                    |
| Description   | Rich Text    | No       | Video description                      |
| URL           | URL          | Yes      | YouTube video URL (watch?v= format)    |
| Category      | Select       | Yes      | "video" or "short" (based on duration) |
| Channel       | Select       | No       | Channel name                           |
| Publish_At    | Date         | No       | Video publish at                       |
| Video_id      | Text         | Yes      | YouTube video ID for deduplication     |
| Tags          | Multi-select | No       | Video tags/keywords from YouTube       |

Tags are individual multi-select options from YouTube video keywords.
