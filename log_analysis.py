#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def get_most_popular_articles():

    """Returns top 3 most popular articles
    and number of views for each article"""

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select s.title, sum(s.views) as views
                    from
                    (select ar.title, count(ar.title) as views
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


def popular_articles_by_author():

    """ Returns author and number of times
    their most popular article was viewed """

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
                        order by 2 desc''')
    popular_by_author = c.fetchall()
    db.close()
    return popular_by_author


def get_most_errors():

    """Returns the date and error percentage for days
    where request had an error rate greater than 1 percent"""

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute('''select
                    t2.error_date,
                    error_percentage||'%' as error_percentage
                from
                (
                select
                    t1.error_date,
                    round(100 * sum(t1.error_count) / sum(views),2)
                    as error_percentage
                from
                (
                    select
                        t.error_date, sum(error_count) as error_count,
                        sum(error_count + non_error_count) as views
                    from
                    (
                    select
                        time::DATE as error_date,
                        case when status LIKE '4%'
                        then 1
                        else 0
                        end as error_count,
                        case when status NOT LIKE '4%'
                        then 1
                        else 0
                        end as non_error_count
                    from LOG
                    )t
                group by 1
                )t1
                group by 1
                )t2
                where t2.error_percentage > 1''')
    error_data = c.fetchall()
    db.close()
    return error_data


def display_results():
    popular_article_result = get_most_popular_articles()
    print("3 most popular articles:")
    print("________________________")
    for article in popular_article_result:
        print(article[0] + ' --', str(article[1]) + ' views')

    popular_author_article = popular_articles_by_author()
    print(' ')
    print("Most popular aticle by author:")
    print('_____________________________')
    for author_article in popular_author_article:
        print(author_article[0] + ' --', str(author_article[1]) + ' views')

    errors = get_most_errors()
    print('')
    print('Days with more than 1 percent request errors:')
    print('____________________________________________')
    for error in errors:
        print(str(error[0]),  str(error[1]))


def main():
    display_results()


if __name__ == '__main__':
    main()
