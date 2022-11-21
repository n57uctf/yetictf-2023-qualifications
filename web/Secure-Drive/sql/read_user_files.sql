SELECT
        f._file as file_id,
        f.owner_ as owner_id,
        f.name as filename,
        f.size as size,
        f.create_date as upload_date
    FROM files f
    WHERE f.owner_ = %(user)s