#!/usr/bin/env python3
import psycopg2

DBNAME = "news"

def get_most_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select s.title, sum(s.views) as views
                    from 
                    (select ar.title, count(ar.title) as views
                        --from authors au
                        from articles ar
                        join log 
                        on ar.slug = right(path, length(path) - 9)
                        group by ar.title
                        order by 2 desc
                    )s
                    group by s.title
                    order by 2 desc
                    limit 3''')
    most_popular_articles = c.fetchall()
    db.close()
    return most_popular_articles

def total_articles_by_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select s.name, sum(s.views) as views
                        from 
                        (select au.name, count(path) as views
                            from authors au
                            join articles ar
                            on au.id  = ar.author
                            join log 
                            on ar.slug = right(path, length(path) - 9)
                            group by au.name
                            order by 2 desc
                        )s
                        group by s.name
                        order by 2 desc;''')
    total_by_author = c.fetchall()
    db.close()
    return total_by_author

def get_most_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''SELECT
                    t2.error_date, 
                    error_percentage||'%' AS error_percentage
                FROM
                (
                SELECT 
                    t1.error_date, 
                    round(100 * SUM(t1.error_count) / SUM(views),2) AS error_percentage
                FROM
                (
                    SELECT 
                        t.error_date, SUM(error_count) AS error_count, 
                        SUM(error_count + non_error_count) AS views
                    FROM
                    (
                    SELECT 
                        time::DATE AS error_date , 
                        CASE WHEN status LIKE '4%'
                        THEN 1
                        ELSE 0
                        END AS error_count,
                
                        CASE WHEN status NOT LIKE '4%'
                        THEN 1 
                        ELSE 0
                        END AS non_error_count
                    FROM LOG
                
                    )T
                GROUP BY 1
                )t1
                GROUP BY 1
                )t2
                WHERE t2.error_percentage > 1''')
    error_data = c.fetchall()
    db.close()
    return error_data

#print(get_most_popular_articles())
#print(total_articles_by_author())
#print(get_most_errors())
    

