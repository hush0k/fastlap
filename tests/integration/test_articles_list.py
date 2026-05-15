from datetime import datetime
from logging import getLogger

from django.test import TestCase
from django.urls import reverse

from apps.news.models import Article, Tag
from apps.races.models import Series
from apps.users.models import User
from tests.config import TEST_LOGGER_NAME

logger = getLogger(TEST_LOGGER_NAME)


class TestArtcilesList(TestCase):
    news_url = reverse("articles-list")

    @classmethod
    def setUpTestData(cls) -> None:
        cls.author1 = User.objects.create_user(
            username="author_lewis",
            email="lewis@example.com",
            password="MyPassword123!",
        )
        cls.author2 = User.objects.create_user(
            username="author_max",
            email="max@example.com",
            password="MyPassword123!",
        )
        cls.author3 = User.objects.create_user(
            username="author_valentino",
            email="valentino@example.com",
            password="MyPassword123!",
        )

        cls.series_f1 = Series.objects.create(name="Formula 1", category="car")
        cls.series_nascar = Series.objects.create(name="NASCAR", category="car")
        cls.series_motogp = Series.objects.create(name="MotoGP", category="moto")
        cls.series_lemans = Series.objects.create(name="Le Mans", category="endurance")

        cls.tag_race = Tag.objects.create(name="Race")
        cls.tag_qualifying = Tag.objects.create(name="Qualifying")
        cls.tag_driver = Tag.objects.create(name="Driver")
        cls.tag_technical = Tag.objects.create(name="Technical")
        cls.tag_safety = Tag.objects.create(name="Safety")

        content_short = "a" * 200
        articles_data = [
            {
                "name": "Monaco Grand Prix Race Review",
                "author": cls.author1,
                "content": "The Monaco Grand Prix delivered another thrilling spectacle on the streets of Monte Carlo. Narrow barriers and zero room for error made every overtake a masterpiece of precision driving. The race saw multiple safety car periods and a dramatic finish that shocked the entire paddock and millions of fans worldwide.",
                "is_published": True,
                "views_count": 1500,
                "published_at": "2024-05-26",
                "tags": [cls.tag_race, cls.tag_driver],
                "series": [cls.series_f1],
            },
            {
                "name": "Red Bull Dominance Technical Analysis",
                "author": cls.author1,
                "content": "Red Bull Racing has achieved an unprecedented level of aerodynamic efficiency with their latest challenger. The underfloor geometry combined with innovative suspension kinematics gives them a distinct advantage in high speed corners. Engineers across rival teams have been studying their car extensively to understand the performance delta.",
                "is_published": True,
                "views_count": 980,
                "published_at": "2024-04-10",
                "tags": [cls.tag_technical],
                "series": [cls.series_f1],
            },
            {
                "name": "NASCAR Daytona 500 Highlights",
                "author": cls.author2,
                "content": "The Great American Race once again proved why it is the most iconic event in American motorsport. Pack racing at two hundred miles per hour with inches separating dozens of cars creates an atmosphere unlike anything else in sports. The final lap draft battles and the photo finish left fans breathless in the stands and at home.",
                "is_published": True,
                "views_count": 2200,
                "published_at": "2024-02-19",
                "tags": [cls.tag_race],
                "series": [cls.series_nascar],
            },
            {
                "name": "MotoGP Qualifying Battle at Mugello",
                "author": cls.author3,
                "content": "Mugello is a cathedral of speed for motorcycle racing and the qualifying session proved exactly why. Riders pushed their machines to the absolute limit across the long straight and the flowing sequence of corners. The gap between pole position and tenth place was less than half a second, illustrating the extraordinary level of competition.",
                "is_published": True,
                "views_count": 760,
                "published_at": "2024-06-01",
                "tags": [cls.tag_qualifying, cls.tag_driver],
                "series": [cls.series_motogp],
            },
            {
                "name": "Le Mans 24 Hours Endurance Preview",
                "author": cls.author2,
                "content": "The 24 Hours of Le Mans remains the ultimate test of man and machine in motorsport. Teams spend entire seasons preparing for this single event where reliability is just as important as outright pace. This year the Hypercar class features more manufacturers than ever, promising a battle that will unfold across an entire day and night.",
                "is_published": True,
                "views_count": 430,
                "published_at": "2024-06-08",
                "tags": [cls.tag_race],
                "series": [cls.series_lemans],
            },
            {
                "name": "F1 Safety Car Regulations Explained",
                "author": cls.author1,
                "content": "The FIA safety car procedures are among the most debated topics in Formula 1. Understanding when a virtual safety car is deployed versus a full safety car, and how lapping works under yellow flag conditions, is essential for following the sport. This article breaks down every regulation and explains the controversies they have caused.",
                "is_published": True,
                "views_count": 320,
                "published_at": "2024-03-15",
                "tags": [cls.tag_safety, cls.tag_technical],
                "series": [cls.series_f1],
            },
            {
                "name": "NASCAR Plate Racing Strategy Guide",
                "author": cls.author2,
                "content": "Superspeedway racing in NASCAR requires a completely different strategic mindset from short track events. Drafting partners, pit cycle timing, and fuel mileage calculations all play a critical role in determining the outcome. The team that manages communication and positioning in the final ten laps almost always has the best chance of winning.",
                "is_published": True,
                "views_count": 540,
                "published_at": "2024-04-28",
                "tags": [cls.tag_technical],
                "series": [cls.series_nascar],
            },
            {
                "name": "MotoGP Rookie Driver Spotlight",
                "author": cls.author3,
                "content": "Every generation brings new talent to MotoGP that challenges the established order of the grid. This season a handful of rookies have already demonstrated pace that rivals experienced race winners. Their adaptation to the physical demands of a MotoGP machine and their mental composure under pressure sets them apart from past generations.",
                "is_published": True,
                "views_count": 290,
                "published_at": "2024-05-05",
                "tags": [cls.tag_driver],
                "series": [cls.series_motogp],
            },
            {
                "name": "Qualifying Lap Breakdown Silverstone",
                "author": cls.author1,
                "content": "Silverstone's qualifying lap is one of the most demanding sequences in Formula 1. From the high speed Copse corner through Maggotts and Becketts to the long Chapel straight, every micro sector requires perfect car setup and driver commitment. We analyse the telemetry sector by sector to understand where lap time is gained and lost.",
                "is_published": True,
                "views_count": 1100,
                "published_at": "2024-07-05",
                "tags": [cls.tag_qualifying, cls.tag_technical],
                "series": [cls.series_f1],
            },
            {
                "name": "Le Mans Hypercar Class Comparison",
                "author": cls.author2,
                "content": "The Hypercar regulations have attracted Ferrari, Toyota, Porsche, Cadillac, and Peugeot to the top class at Le Mans. Each manufacturer has taken a different technical approach within the ruleset, resulting in cars with distinct characteristics on the Sarthe circuit. This comparison analyses their aerodynamic packages, hybrid systems, and driver lineups.",
                "is_published": True,
                "views_count": 670,
                "published_at": "2024-06-10",
                "tags": [cls.tag_technical],
                "series": [cls.series_lemans],
            },
            {
                "name": "F1 Driver Championship Standings Update",
                "author": cls.author1,
                "content": "After the first half of the season the championship picture is becoming clearer but remains far from decided. Points gaps that seemed insurmountable three races ago have closed dramatically following a string of mechanical failures and strategic errors. The second half of the calendar includes circuits that historically favour different car characteristics.",
                "is_published": True,
                "views_count": 1800,
                "published_at": "2024-07-20",
                "tags": [cls.tag_driver, cls.tag_race],
                "series": [cls.series_f1],
            },
            {
                "name": "MotoGP Technical Regulation Changes",
                "author": cls.author3,
                "content": "The upcoming technical regulation changes in MotoGP will affect electronics, aerodynamics, and engine specifications significantly. Manufacturers have been lobbying for different interpretations of the new rules during the consultation period. The changes are designed to reduce costs and close the performance gap between factory and satellite teams.",
                "is_published": False,
                "views_count": 0,
                "published_at": None,
                "tags": [cls.tag_technical, cls.tag_safety],
                "series": [cls.series_motogp],
            },
            {
                "name": "NASCAR Next Gen Car Safety Review",
                "author": cls.author2,
                "content": "The Next Gen car introduced significant safety improvements over its predecessor through a completely redesigned roll cage and updated HANS device mounting points. Real world crash data collected over the past two seasons has validated many of the design choices. However engineers continue to refine specific areas where improvements are still possible.",
                "is_published": True,
                "views_count": 410,
                "published_at": "2024-03-30",
                "tags": [cls.tag_safety, cls.tag_technical],
                "series": [cls.series_nascar],
            },
            {
                "name": "Race Strategy Pit Stop Windows Explained",
                "author": cls.author3,
                "content": "Understanding pit stop windows is fundamental to appreciating the strategic dimension of motorsport. The undercut and overcut are tools teams use to gain track position without relying solely on raw pace. Tyre degradation models, traffic predictions, and safety car probability all feed into the strategic decisions made on pit wall.",
                "is_published": True,
                "views_count": 55,
                "published_at": "2024-01-15",
                "tags": [cls.tag_race, cls.tag_technical],
                "series": [cls.series_f1, cls.series_nascar],
            },
            {
                "name": "Driver Contract Silly Season Preview",
                "author": cls.author1,
                "content": "The driver market in motorsport is one of the most compelling off track storylines of every season. Several high profile seats are expected to become available and the list of drivers without confirmed deals for next year is longer than usual. We examine each team's situation, their priorities, and which drivers are most likely to move.",
                "is_published": False,
                "views_count": 0,
                "published_at": None,
                "tags": [cls.tag_driver],
                "series": [cls.series_f1, cls.series_motogp],
            },
            {
                "name": "Endurance Racing Tyre Management Secrets",
                "author": cls.author2,
                "content": "Managing tyres across a long stint in endurance racing requires a completely different philosophy from sprint racing. Drivers must balance pace with conservation across stints that can last over an hour at circuits that are notoriously demanding on rubber. Team engineers play a critical role in coaching drivers through temperature windows and degradation cliffs.",
                "is_published": True,
                "views_count": 380,
                "published_at": "2024-05-18",
                "tags": [cls.tag_technical, cls.tag_race],
                "series": [cls.series_lemans],
            },
            {
                "name": "MotoGP Aerodynamics Wings and Holeshots",
                "author": cls.author3,
                "content": "Aerodynamic development in MotoGP has accelerated dramatically over the past five years. Front wings, rear wings, and the holeshot device have fundamentally changed how bikes are set up and ridden. The holeshot system in particular has transformed race starts by allowing riders to lower the bike mechanically for maximum traction off the line.",
                "is_published": True,
                "views_count": 620,
                "published_at": "2024-04-22",
                "tags": [cls.tag_technical],
                "series": [cls.series_motogp],
            },
            {
                "name": "F1 Qualifying Format History and Changes",
                "author": cls.author1,
                "content": "Formula 1 qualifying has gone through numerous format changes since the championship began. From aggregate times and single lap shootouts to the current three segment elimination format, each era reflects the sport's priorities at that time. The sprint race weekend format adds another layer of complexity to the modern qualifying picture.",
                "is_published": True,
                "views_count": 210,
                "published_at": "2024-02-05",
                "tags": [cls.tag_qualifying],
                "series": [cls.series_f1],
            },
            {
                "name": "NASCAR Short Track Racing Craft",
                "author": cls.author2,
                "content": "Short track racing is widely considered the purest form of NASCAR competition where raw talent matters more than horsepower or aerodynamic efficiency. Bristol, Martinsville, and Richmond separate the elite drivers from the rest of the field through their demand for precise car control and wheel to wheel racecraft over hundreds of laps.",
                "is_published": True,
                "views_count": 730,
                "published_at": "2024-03-18",
                "tags": [cls.tag_race, cls.tag_driver],
                "series": [cls.series_nascar],
            },
            {
                "name": "Safety Standards Evolution in Motorsport",
                "author": cls.author3,
                "content": "The history of motorsport safety is a story of tragedy driving innovation. From the introduction of crash helmets and fire resistant suits to the modern halo device and advanced barriers, every major improvement has come in response to accidents that cost lives. Today the sport is safer than it has ever been but the pursuit of improvement never stops.",
                "is_published": True,
                "views_count": 890,
                "published_at": "2024-01-30",
                "tags": [cls.tag_safety],
                "series": [cls.series_f1, cls.series_motogp, cls.series_nascar],
            },
        ]

        assert len(articles_data) == 20

        for data in articles_data:
            tags = data.pop("tags")
            series = data.pop("series")
            article = Article.objects.create(**data)
            article.tags.set(tags)
            article.series.set(series)

    def test_get_only_published_articles(self) -> None:
        response = self.client.get(self.news_url)
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 18)

    def test_filter_one_series(self) -> None:
        series = "NASCAR"
        response = self.client.get(self.news_url + f"?series={series}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        for article in response.json()["results"]:
            self.assertIn(series, [i["name"] for i in article["series"]])

    def test_filter_several_series(self) -> None:
        series1 = "NASCAR"
        series2 = "Formula 1"
        response = self.client.get(self.news_url + f"?series={series1},{series2}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        for article in response.json()["results"]:
            article_series: set[str] = {i["name"] for i in article["series"]}
            self.assertTrue({series1, series2} & article_series)

    def test_filter_with_tags(self) -> None:
        tag = "Qualifying"
        response = self.client.get(self.news_url + f"?tags={tag}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        for article in response.json()["results"]:
            self.assertIn(tag, [i["name"] for i in article["tags"]])

    def test_search_with_correct_name(self) -> None:
        name = "MotoGP Rookie Driver Spotlight"
        response = self.client.get(self.news_url + f"?search={name}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 1)
        self.assertEqual(response.json()["results"][0]["name"], name)

    def test_search_with_name_part(self) -> None:
        name_part = "MotoGP"
        response = self.client.get(self.news_url + f"?search={name_part}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        # it returns 3 not 4 because 1 article is not published
        self.assertEqual(response.json()["count"], 3)
        for article in response.json()["results"]:
            self.assertIn(name_part, article["name"])

    def test_filter_published_after(self) -> None:
        date_str = "2024-06-01"
        response = self.client.get(self.news_url + f"?published_after={date_str}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 5)
        for article in response.json()["results"]:
            article_date = datetime.fromisoformat(article["published_at"]).date()
            self.assertGreaterEqual(
                article_date, datetime.fromisoformat(date_str).date()
            )

    def test_filter_published_before(self) -> None:
        date_str = "2024-03-15"
        response = self.client.get(self.news_url + f"?published_before={date_str}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 5)
        for article in response.json()["results"]:
            article_date = datetime.fromisoformat(article["published_at"]).date()
            self.assertLessEqual(article_date, datetime.fromisoformat(date_str).date())

    def test_filter_min_views(self) -> None:
        min_views = 1000
        response = self.client.get(self.news_url + f"?min_views={min_views}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 4)
        for article in response.json()["results"]:
            self.assertGreaterEqual(article["views_count"], min_views)

    def test_filter_max_views(self) -> None:
        max_views = 300
        response = self.client.get(self.news_url + f"?max_views={max_views}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 3)
        for article in response.json()["results"]:
            self.assertLessEqual(article["views_count"], max_views)

    def test_filter_author_id(self) -> None:
        author_id = self.author1.id
        response = self.client.get(self.news_url + f"?author_id={author_id}")
        logger.debug("%s: %s", self._testMethodName, response.text)

        self.assertEqual(response.json()["count"], 6)
        for article in response.json()["results"]:
            self.assertEqual(article["author"]["id"], author_id)
