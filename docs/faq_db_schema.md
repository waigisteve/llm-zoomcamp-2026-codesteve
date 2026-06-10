# FAQ Database Schema

Database file: `faq.db`

This SQLite database stores FAQ documents and a full-text search index for retrieval. The main source table is `docs`; the `docs_fts*` tables are SQLite FTS5 backing tables.

## Tables

| Table | Purpose | Rows |
| --- | --- | ---: |
| `docs` | Stores original FAQ records as JSON plus a course filter field. | 158 |
| `docs_fts` | FTS5 virtual table used for full-text search over question, section, and answer fields. | 158 |
| `docs_fts_data` | Internal FTS5 segment data table. | Internal |
| `docs_fts_idx` | Internal FTS5 segment index table. | Internal |
| `docs_fts_content` | Internal FTS5 content table. | Internal |
| `docs_fts_docsize` | Internal FTS5 document size table. | Internal |
| `docs_fts_config` | Internal FTS5 config table. | Internal |
| `sqlite_sequence` | SQLite internal table for autoincrement counters. | Internal |

## Main Table: `docs`

| Column | Type | Required | Key | Description |
| --- | --- | --- | --- | --- |
| `id` | `INTEGER` | No | Primary key | Autoincrementing row id. |
| `doc_json` | `TEXT` | Yes |  | Full FAQ document serialized as JSON. |
| `course` | `TEXT` | No | Indexed | Course identifier used for filtering, for example `llm-zoomcamp`. |

DDL:

```sql
CREATE TABLE docs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_json TEXT NOT NULL,
    "course" TEXT
);
```

## Full-Text Search Table: `docs_fts`

| Column | Type | Description |
| --- | --- | --- |
| `docid` | untyped | Links the FTS row to the source document id. |
| `question` | untyped | FAQ question text. |
| `section` | untyped | FAQ section text. |
| `answer` | untyped | FAQ answer text. |

DDL:

```sql
CREATE VIRTUAL TABLE docs_fts USING fts5(
    docid,
    "question",
    "section",
    "answer",
    tokenize='unicode61'
);
```

## Indexes

```sql
CREATE INDEX idx_course ON docs ("course");
```

`idx_course` supports filtering FAQ documents by course.

## Internal FTS5 Tables

SQLite creates these tables automatically to support the `docs_fts` virtual table:

```sql
CREATE TABLE 'docs_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE 'docs_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE 'docs_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3);
CREATE TABLE 'docs_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE 'docs_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
```

These are implementation details of SQLite FTS5 and should not usually be queried directly.

## Example Stored Document

Rows in `docs.doc_json` contain JSON records with fields like:

```json
{
  "id": "74eb249bbf",
  "course": "llm-zoomcamp",
  "section": "General Course-Related Questions",
  "question": "I just discovered the course. Can I still join?",
  "answer": "..."
}
```

## Useful Inspection Queries

List tables:

```bash
sqlite3 faq.db ".tables"
```

Show schema:

```bash
sqlite3 faq.db ".schema"
```

Count records:

```sql
SELECT COUNT(*) FROM docs;
SELECT COUNT(*) FROM docs_fts;
```

Preview documents:

```sql
SELECT id, course, substr(doc_json, 1, 200)
FROM docs
LIMIT 5;
```

Run a full-text search:

```sql
SELECT docid, question, section, answer
FROM docs_fts
WHERE docs_fts MATCH 'join course'
LIMIT 5;
```
