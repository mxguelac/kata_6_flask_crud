CREATE TABLE "movements" (
	"id"	INTEGER UNIQUE,
	"date"	TEXT NOT NULL,
	"abstract"	TEXT NOT NULL,
	"amount "	REAL NOT NULL,
	"currency"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);