# News Database Schema

Based on `article_data` structure from `src/clients/news.py`:

| Property Name | Type      | Required | Description                  |
| ------------- | --------- | -------- | ---------------------------- |
| Title         | Title     | Yes      | Article title                |
| Description   | Rich Text | No       | Article description          |
| URL           | URL       | Yes      | Article URL                  |
| Source        | Select    | Yes      | News source name             |
| Publish_At    | Date      | Yes      | Article publish date         |
| Article_Id    | Text      | Yes      | Article ID for deduplication |
| Source_URL    | Text      | No       | Source website URL           |

Note: Each database has its own ID property (Video_id for YouTube, Article_Id for News).

Optional properties (Source_URL) are only added when available.
