SELECT
        f._file as file_id,
        f.content as content,
        f.name as filename
    FROM files f
    WHERE f._file = %(files_id)s
