GET_MUSIC_CURRENT_USER ="""
    SELECT
        m.name AS music_name,
        m.albom AS album,
        m.artist AS artist,
        STRING_AGG(g.genre, ', ') AS genres
    FROM
        users u
    JOIN
        user_musics um ON u.id = um.user_id
    JOIN
        musics m ON um.music_id = m.id
    LEFT JOIN
        music_genres mg ON m.id = mg.music_id
    LEFT JOIN
        genres g ON mg.genre_id = g.id
    WHERE
        u.id = :user_id
    GROUP BY
        m.name, m.albom, m.artist;
"""