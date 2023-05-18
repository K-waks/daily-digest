import psycopg2 as db
import os


"""
my idea here below was that if this app was being downloaded from the internet, there would be different optiond here like 'download for windows, or for linux or macos'. And so depending on your os the path here for the app's database and temporary (temp) files would be based on how the OS's file system is structures
"""

temp = "C:\Daily Digest"  # so here will be the path where windows applications store there system files

try:
    os.mkdir(temp)
except Exception as e:
    pass


def create_database():
    connection = db.connect(
        user="postgres",
        password="huperetes",
        host="localhost",
        database="dailydigest",
        port="5432",
    )

    cursor = connection.cursor()

    cursor.execute("""DROP TABLE IF EXISTS verses;""")

    cursor.execute("""DROP TABLE IF EXISTS lessons;""")

    cursor.execute("""DROP TABLE IF EXISTS devotions;""")

    cursor.execute("""DROP TABLE IF EXISTS subscribers;""")

    cursor.execute("""DROP TABLE IF EXISTS administrators;""")

    cursor.execute(
        """CREATE TABLE administrators (admin_id SERIAL NOT NULL PRIMARY KEY, username TEXT, password TEXT);"""
    )
    cursor.execute(
        """INSERT INTO administrators (username, password) VALUES
                ('admin', 'password'),
                ('kevin', 'wakhisi'),
                ('linda', 'esipira');"""
    )

    cursor.execute(
        """CREATE TABLE verses (verses_id SERIAL NOT NULL PRIMARY KEY, reference TEXT, verse TEXT);"""
    )
    cursor.execute(
        """INSERT INTO verses (reference, verse) VALUES
                ('Hebrews 13:8', 'Jesus Christ is the same yesterday and today and forever.'),
                ('1 Chronicles 16:11', 'Seek the LORD and his strength seek his presence continually!'),
                ('1 Thessalonians 5:16', 'Rejoice always'),
                ('Psalm 56:3', 'When I am afraid I put my trust in you.'),
                ('Psalm 37:3', 'Trust in the LORD and do good; dwell in the land and befriend faithfulness'),
                ('Jeremiah 29:11', 'For I know the plans I have for you; declares the LORD; plans to prosper you and not to harm you; plans to give you hope and a future.'),
                ('John 3:16', 'For God so loved the world that he gave his one and only Son; that whoever believes in him shall not perish but have eternal life.'),
                ('Matthew 5:14', 'You are the light of the world. A town built on a hill cannot be hidden.'),
                ('Proverbs 3:5', 'Trust in the LORD with all your heart and lean not on your own understanding'),
                ('Proverbs 18:10', 'The name of the LORD is a fortified tower; the righteous run to it and are safe.'),
                ('Proverbs 27:17', 'As iron sharpens iron so one person sharpens another.'),
                ('Psalm 119:105', 'Your word is a lamp for my feet; a light on my path.'),
                ('Psalm 136:1', 'Give thanks to the LORD for he is good. His love endures forever.'),
                ('Isaiah 43:10', 'Fear thou not for I am with thee. Be not dismayed for I am thy God. I will strengthen thee; yea I will hep thee yea I will uphold thee with the right hand of my righteousness'),
                ('Psalm 56:3', 'When I am afraid I put my trust in you.');"""
    )

    cursor.execute(
        """ CREATE TABLE devotions (devotions_id SERIAL NOT NULL PRIMARY KEY, weekday TEXT, readings TEXT);"""
    )

    cursor.execute(
        """INSERT INTO devotions (weekday, readings) VALUES
                                                        ('Monday','The only way a person can shine brightly in the light of Christ is to also live for Him and not the world. It is willful sin that tears us away from God and causes our light to go dim and then out completely. Paul said, for ye were sometimes darkness, but now are ye light in the Lord: walk as children of light: (For the fruit of the Spirit is in all goodness and righteousness and truth;) Proving what is acceptable unto the Lord. And have no fellowship with the unfruitful works of darkness, but rather reprove them. For it is a shame even to speak of those things which are done of them in secret. But all things that are reproved are made manifest by the light: for whatsoever doth make manifest is light. Wherefore he saith, Awake thou that sleepest, and arise from the dead, and Christ shall give thee light. (Ephesians 5:8-14) Do we accept any form of evil in our lives? No. Do we do things in secret and say we will just repent later? No. To walk in the light of Jesus is to also do His will and not the things of the flesh. It is only God who can lead us from temptation and keep our light shining brightly for Him as long as we have breath. Amen.'),
                                                        ('Tuesday','During the times of the old covenant on earth, there was Gods tabernacle. Inside of this building was a candlestick that the high priest would light the lamps thereon. These lights were never to go out. It is written, and the Lord spake unto Moses, saying, speak unto Aaron and say unto him, When thou lightest the lamps, the seven lamps shall give light over against the candlestick. And Aaron did so; he lighted the lamps thereof over against the candlestick, as the Lord commanded Moses. And this work of the candlestick was of beaten gold, unto the shaft thereof, unto the flowers thereof, was beaten work: according unto the pattern which the Lord had shewed Moses, so he made the candlestick. (Numbers 8:1-4) And now in our time, these candlesticks continue in us. We are the light of the world and therefore we shine brightly before God and man. This way more people will come to God also for salvation and serve Him.'),
                                                        ('Wednesday','To speak evil about Gods servants is also doing a disservice to God Himself. This is telling God that whom He chose to do His will on earth was wrong. Many people do this and try to find fault in people who are really trying their best to live for God. Miriam and Aaron did this against Moses because of his Ethiopian wife. These two people were called out by God in His wrath. It is written, and Miriam and Aaron spake against Moses because of the Ethiopian woman whom he had married: for he had married an Ethiopian woman. And they said, Hath the Lord indeed spoken only by Moses? hath he not spoken also by us? And the Lord heard it. (Now the man Moses was very meek, above all the men which were upon the face of the earth.) And the Lord spake suddenly unto Moses, and unto Aaron, and unto Miriam, Come out ye three unto the tabernacle of the congregation. And they three came out. (Numbers 12:1-4) Imagine doing something wrong and then being called out by God in all His wrath. It would be terrifying.'),
                                                        ('Thursday','Most people, including atheists, the LGBTQ, and others know about Matthew, chapter 7. They like to use verse 1 against Christian evangelists who are sharing the gospel message to the lost. They hate it when we tell them what sin is in the sight of God, for they feel judged. This judgment, they feel is wrong and goes against what Jesus said. However, their issue is that they did not keep reading through verse 5. Those verses read, judge not, that ye be not judged. For with what judgment ye judge, ye shall be judged: and with what measure ye mete, it shall be measured to you again. And why beholdest thou the mote that is in thy brothers eye, but considerest not the beam that is in thine own eye? Or how wilt thou say to thy brother, Let me pull out the mote out of thine eye; and, behold, a beam is in thine own eye? Thou hypocrite, first cast out the beam out of thine own eye; and then shalt thou see clearly to cast out the mote out of thy brothers eye. (Matthew 7:1-5) So if we have not gotten right with God in the same or different area with God then we have no right to be judging anyone else.'),
                                                        ('Friday','Every person that asks of the Lord, will gain different spiritual gifts like Solomon did. All he wanted was to gain wisdom and enough knowledge to judge the people, which God was happy about. So 1Solomon said unto God, Thou hast shewed great mercy unto David my father, and hast made me to reign in his stead. Now, O Lord God, let thy promise unto David my father be established: for thou hast made me king over a people like the dust of the earth in multitude. Give me now wisdom and knowledge, that I may go out and come in before this people: for who can judge this thy people, that is so great? And God said to Solomon, Because this was in thine heart, and thou hast not asked riches, wealth, or honour, nor the life of thine enemies, neither yet hast asked long life; but hast asked wisdom and knowledge for thyself, that thou mayest judge my people, over whom I have made thee king: Wisdom and knowledge is granted unto thee; and I will give thee riches, and wealth, and honour, such as none of the kings have had that have been before thee, neither shall there any after thee have the like. (2 Chronicles 1:8-12) My friends, God did deliver what Solomon desired, for it pleased Him. And because he didnt want anything else, God blessed him abundantly with not just wisdom and knowledge. He was given all the money and honor that a king would ever want. So does God still work like this? He sure does. If your heart is in the right place with God and your desires are sincere, you will gain the gift that you desire, along with even more blessings, which will pour down upon you. The Lord just desires that we acknowledge Him and trust that He will answer our prayers. Then He will respond in our favor like He did with Solomon and David in his lifetime.')
                                                        ;"""
    )

    cursor.execute(
        """ CREATE TABLE subscribers (subscribers_id SERIAL NOT NULL PRIMARY KEY, email TEXT);"""
    )

    cursor.execute(
        """INSERT INTO subscribers (email) VALUES
                                                        ('wakskevin@students.uonbi.ac.ke'),
                                                        ('wakskevin202@gmail.com'),
                                                        ('wakskevin@outlook.com'),
                                                        ('jessica@treeolive.com'),
                                                        ('jon@treeolive.com'),
                                                        ('daphne@treeolive.com'),
                                                        ('edwin@treeolive.com'),
                                                        ('linda@treeolive.com'),
                                                        ('evans@treeolive.com');"""
    )

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_database()
