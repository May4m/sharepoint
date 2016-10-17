BEGIN;
--
-- Create model FileModel
--
CREATE TABLE "sharepointer_filemodel" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "file" varchar(100) NOT NULL,
    "date_uploaded" datetime NOT NULL,
    "views" integer NOT NULL);
--
-- Delete model FileEntity
--
DROP TABLE "sharepointer_fileentity";
--
-- Create model ReceivedFile
--
CREATE TABLE "sharepointer_receivedfile" (
    "filemodel_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "sharepointer_filemodel" ("id"));
--
-- Create model SentFile
--
CREATE TABLE "sharepointer_sentfile" (
    "filemodel_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "sharepointer_filemodel" ("id"));
--
-- Add field owner to filemodel
--
ALTER TABLE "sharepointer_filemodel" RENAME TO "sharepointer_filemodel__old";

CREATE TABLE "sharepointer_filemodel" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "file" varchar(100) NOT NULL, "date_uploaded" datetime NOT NULL,
    "views" integer NOT NULL,
    "owner_id" integer NOT NULL REFERENCES "auth_user" ("id"));

INSERT INTO "sharepointer_filemodel" ("owner_id", "date_uploaded", "id", "file", "views") SELECT NULL, "date_uploaded", "id", "file", "views" FROM "sharepointer_filemodel__old";

DROP TABLE "sharepointer_filemodel__old";

CREATE INDEX "sharepointer_filemodel_owner_id_a4f2ef2e" ON "sharepointer_filemodel" ("owner_id");
COMMIT;
