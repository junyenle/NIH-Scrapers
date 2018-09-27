# patch.com news scraper
# written by Jun Yen Leung for CSSL (USC)

###### IMPORTS ######
from bs4 import BeautifulSoup
import mysql.connector
import urllib.request
from datetime import datetime
import json


###### SETTINGS ######
SQL_CONFIG = {
	'user':'root',
	'password':'root',
	'host':'localhost',
	'database':'Patch',
	'raise_on_warnings':True,
	'charset':'utf8mb4',
	'collation':'utf8mb4_bin'
}

###### GLOBALS ######
MOVIES = ['The Social Network', 'A Separation', 'The Artist', 'Toy Story 3', "The King's Speech", 'Up', 'No Country for Old Men', 'The Lord of the Rings: The Return of the King', 'Crouching Tiger, Hidden Dragon', 'The Dark Knight', "Pan's Labyrinth", 'Finding Nemo', 'Sideways', 'Spirited Away', 'True Grit', 'Harry Potter and the Deathly Hallows: Part 2', 'The Hurt Locker', 'The Wrestler', 'There Will Be Blood', 'Ratatouille', 'The Queen', 'Eternal Sunshine of the Spotless Mind', 'Lost in Translation', 'The Lord of the Rings: The Two Towers', 'Argo', "Winter's Bone", 'Hugo', 'Once', 'Before Sunset', 'City of God', 'Million Dollar Baby', 'The Incredibles', 'American Splendor', 'A Prophet', 'Drive', '127 Hours', 'Black Swan', 'The Diving Bell and the Butterfly', 'Slumdog Millionaire', 'The Lives of Others', 'Letters from Iwo Jima', 'The Departed', 'Capote', 'United 93', 'Brokeback Mountain', 'Ying xiong', 'The Triplets of Belleville', 'Spider-Man 2', 'The Pianist', 'Adaptation.', 'Another Year', 'Let the Right One In', 'Memento', 'Monsieur Lazhar', 'Persepolis', 'Skyfall', 'Beasts of the Southern Wild', 'Moonrise Kingdom', 'The Descendants', 'The Tree of Life', 'Up in the Air', 'Star Trek', 'Juno', 'The Curse of the Were-Rabbit', 'Good Night, and Good Luck.', 'Talk to Her', 'Far from Heaven', 'The Lord of the Rings: The Fellowship of the Ring', 'Des hommes et des dieux', 'Away from Her', 'Looper', 'You Can Count on Me', 'Holy Motors', 'Spring, Summer, Fall, Winter... and Spring', 'The Avengers', 'Moneyball', 'Inception', 'Milk', 'The Bourne Ultimatum', 'Borat: Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan', 'Children of Men', 'The Dark Knight Rises', 'Maria Full of Grace', 'Hotel Rwanda', 'The Station Agent', 'Downfall', 'Minority Report', 'Take Shelter', 'Raising Victor Vargas', 'Animal Kingdom', 'The Master', 'Silver Linings Playbook', 'Traffic', 'Chicken Run', 'Lincoln', 'The Sessions', 'The Man Without a Past', 'Offside', 'The Kid with a Bike', 'Nobody Knows', 'How to Train Your Dragon', 'The Muppets', 'Fantastic Mr. Fox', 'A Serious Man', 'Frost/Nixon', 'The Squid and the Whale', 'A History of Violence', 'Monsoon Wedding', 'Catch Me If You Can', 'Monsters, Inc.', 'In the Bedroom', 'Bikur Ha-Tizmoret', 'Incendies', "L'illusionniste", 'Vera Drake', 'Life of Pi', 'Bloody Sunday', 'Revanche', 'Mother', 'The Town', 'The Fighter', 'The Kids Are All Right', 'The Secret in Their Eyes', 'Tinker Tailor Soldier Spy', 'Midnight in Paris', 'Win Win', 'An Education', 'Precious', 'District 9', 'Volver', 'Casino Royale', 'The Aviator', 'Harry Potter and the Prisoner of Azkaban', 'School of Rock', 'Dirty Pretty Things', 'House of Flying Daggers', 'Chicago', 'Ghost World', 'In the Loop', 'The Host', 'Hunger', 'Amores Perros', 'Hedwig and the Angry Inch', 'Almost Famous', 'Russkiy kovcheg', 'Osama', 'Mission: Impossible - Ghost Protocol', 'The Cabin in the Woods', 'The Guard', 'Blue Valentine', 'The Counterfeiters', 'Coraline', 'Hairspray', 'Inglourious Basterds', "Before the Devil Knows You're Dead", 'Sweeney Todd: The Demon Barber of Fleet Street', 'Gone Baby Gone', 'Hot Fuzz', 'Knocked Up', 'Little Miss Sunshine', 'Pride & Prejudice', 'Batman Begins', 'In America', 'Kill Bill: Vol. 1', 'King Kong', 'Mystic River', 'Kill Bill: Vol. 2', 'Shaun of the Dead', 'About a Boy', 'The Quiet American', 'Whale Rider', 'About Schmidt', 'Insomnia', 'Happy-Go-Lucky', 'Martha Marcy May Marlene', 'Summer Hours', 'Shrek', 'Footnote', 'Gomorrah', 'Shattered Glass', 'Frankenweenie', 'Rogue', 'Panic', 'In the Mood for Love', 'This Is England', 'The Secret World of Arrietty', 'The Girl with the Dragon Tattoo', 'Bernie', 'Rango', 'Let Me In', '50/50', 'Iron Man', 'Tell No One', 'Drag Me to Hell', 'Michael Clayton', 'Ponyo', 'The Visitor', 'Eastern Promises', 'Zodiac', 'Kung Fu Hustle', 'Shrek 2', 'The Constant Gardener', 'Master and Commander: The Far Side of the World', 'Kinsey', 'Rabbit-Proof Fence', 'Spider-Man', 'Rabbit Hole', 'The White Ribbon', 'Half Nelson', 'Look at Me', 'Water', 'The Wind that Shakes the Barley', 'The Sea Inside', 'The Magdalene Sisters', "Meek's Cutoff", 'Donnie Darko', 'Fish Tank', 'High Fidelity', 'Rust and Bone', 'Compliance', 'Hodejegerne', 'Scott Pilgrim vs. the World', 'Bridesmaids', 'Tangled', 'Source Code', '(500) Days of Summer', 'The Simpsons Movie', '3:10 to Yuma', 'Rescue Dawn', 'Into the Wild', 'The Savages', 'Superbad', 'Notes on a Scandal', 'Sin City', 'Bad Education', '21 Grams', 'Broken Flowers', 'The Motorcycle Diaries', 'Nirgendwo in Afrika', 'Gosford Park', 'X2', 'Road to Perdition', 'Safety Not Guaranteed', 'Junebug', 'Man on the Train', "I'm Not Scared", 'Spider', 'The Messenger', 'The Damned United', 'Wreck-It Ralph', 'Tristram Shandy: A Cock and Bull Story', 'In This World', 'Best in Show', "The Devil's Backbone", 'Paradise Now', "L'enfant", 'Nine Queens', 'X: First Class', 'Avatar', 'Super 8', 'The Ghost Writer', 'Zombieland', 'Crazy Heart', 'Moon', 'Atonement', 'Rachel Getting Married', 'The Namesake', 'Little Children', 'Harry Potter and the Goblet of Fire', 'Cinderella Man', 'Finding Neverland', 'A Very Long Engagement', 'Munich', 'Millions', 'The Three Burials of Melquiades Estrada', "Howl's Moving Castle", 'Garden State', 'Collateral', 'Punch-Drunk Love', "Monster's Ball", 'The Hours', 'A Mighty Wind', 'Mulholland Dr.', 'The Trip', 'La piel que habito', 'Shame', 'Please Give', 'Sin Nombre', "Il y a longtemps que je t'aime", 'The Raid: Redemption', 'After the Wedding', 'Tsotsi', 'Me and You and Everyone We Know', 'Good Bye Lenin!', 'Thirteen Conversations About One Thing', 'Coriolanus', 'Boy A', 'Attack the Block', 'Red Riding: The Year of Our Lord 1974', 'The Perks of Being a Wallflower', 'My Summer of Love', '2046', 'Roger Dodger', 'Cast Away', 'Waking Life', 'George Washington', 'Lantana', 'The Dish', 'Head-On', 'Control', 'Beginners', 'Get Low', 'The Hunger Games', 'Warrior', 'Margin Call', 'The Ides of March', 'Jane Eyre', 'Adventureland', 'The Orphanage', 'A Single Man', 'Cloudy with a Chance of Meatballs', 'Enchanted', 'The Princess and the Frog', 'Waitress', 'The Last King of Scotland', 'Kiss Kiss Bang Bang', 'Thank You for Smoking', 'Inside Man', 'Ray', 'The Descent', 'Walk the Line', 'Hustle & Flow', '28 Days Later...', 'Lilo & Stitch', 'Melancholia', 'Frozen River', 'ParaNorman', 'We Need to Talk About Kevin', 'Bad Lieutenant: Port of Call New Orleans', 'The Lookout', 'Venus', 'The Proposition', 'Sweet Land', 'The Woodsman', 'Confidences trop intimes', 'Thirteen', 'Lovely & Amazing', 'Ruby Sparks', 'Submarine', 'Farewell, My Queen', 'Buried', 'Mesrine Part 1: Killer Instinct', 'The Square', 'Wendy and Lucy', 'Starting Out in the Evening', 'State and Main', 'Billy Elliot', 'Girlfight', 'Oldeuboi', 'Mean Creek', 'The Believer', '24 Hour Party People', 'Requiem for a Dream', 'Erin Brockovich', 'Old Joy', 'Harry Potter and the Deathly Hallows: Part 1', 'The Pirates! Band of Misfits', 'Arthur Christmas', 'Winnie the Pooh', '21 Jump Street', 'The Girl with the Dragon Tattoo', 'Kung Fu Panda', 'Hellboy II: The Golden Army', 'Bolt', 'The Hoax', 'Dreamgirls', 'The Bourne Supremacy', 'Match Point', 'Corpse Bride', 'Charlie and the Chocolate Factory', 'Friday Night Lights', 'Monster', 'Big Fish', 'The 40-Year-Old Virgin', 'Star Wars: Episode III - Revenge of the Sith', 'Bend It Like Beckham', 'The Royal Tenenbaums', 'Confessions of a Dangerous Mind', '25th Hour', 'The Others', 'Spy Kids', 'Sexy Beast', 'Transsiberian', 'Bright Star', 'The Barbarian Invasions', 'The Secret Lives of Dentists', 'Mostly Martha', 'Mysterious Skin', 'Mesrine Part 2: Public Enemy #1', 'Robot & Frank', 'Big Fan', 'Red Cliff', 'Black Dynamite', 'Sleepwalk with Me', 'Beyond the Gates', 'Thirteen Days', 'Nurse Betty', 'La veuve de Saint-Pierre', 'Wonder Boys', 'A Royal Affair', 'Four Lions', 'The Blind Swordsman: Zatoichi', 'Contagion', 'My Week with Marilyn', 'Rise of the Planet of the Apes', "Io sono l'amore", 'Chronicle', 'The Curious Case of Benjamin Button', 'Tropic Thunder', 'Whip It', 'Gran Torino', 'In Bruges', 'Harry Potter and the Half-Blood Prince', 'Lars and the Real Girl', 'Bridge to Terabithia', 'The Painted Veil', 'The Prestige', 'A Prairie Home Companion', 'House of Sand and Fog', 'Crash', 'Serenity', 'The Manchurian Candidate', 'Superman Returns', 'Pirates of the Caribbean: The Curse of the Black Pearl', 'Seabiscuit', 'Narc', 'Iris', 'Matchstick Men', 'Harry Potter and the Chamber of Secrets', 'Swimming Pool', 'Gangs of New York', 'The Rookie', 'A Beautiful Mind', 'Moulin Rouge!', "The Man Who Wasn't There", 'O Brother, Where Art Thou?', 'La doppia ora', 'The Assassination of Jesse James by the Coward Robert Ford', 'The Deep End', "Your Sister's Sister", 'Roman de gare', 'Black Book', 'Layer Cake', 'Brick', 'Pieces of April', 'End of Watch', 'Terri', 'Me and Orson Welles', 'Flight', 'Inland Empire', 'Innocence', 'All or Nothing', 'The Loneliest Planet', 'Looking for Eric', "O'Horten", 'Young Adult', 'The Help', 'The Adventures of Tintin', 'War Horse', 'Cyrus', 'Easy A', 'Captain America: The First Avenger', 'Kick-Ass', 'Broken Embraces', 'The Great Debaters', "Charlie Wilson's War", 'Forgetting Sarah Marshall', 'Paranormal Activity', 'Horton Hears a Who!', 'In the Valley of Elah', 'Mongol: The Rise of Genghis Khan', 'American Gangster', '3 Idiots', 'A Mighty Heart', 'Breach', "Charlotte's Web", 'Akeelah and the Bee', 'The Chronicles of Narnia: The Lion, the Witch and the Wardrobe', 'Flags of our Fathers', 'In Good Company', 'Freaky Friday', 'War of the Worlds', 'Miracle', 'Holes', 'The Bourne Identity']
BADTITLES = []
BADFILE = "badtitles.json"
GOODCOUNT = 0
BADCOUNT = 0
SQL_CONNECTION = ""
SQL_CURSOR = ""


###### METHODS ######
# make a string sql safe
def formatScript(string):
	return string.replace('"', "'")

# initialize connections
def init():
	global SQL_CONNECTION
	global SQL_CURSOR
	SQL_CONNECTION = mysql.connector.connect(**SQL_CONFIG)
	SQL_CURSOR = SQL_CONNECTION.cursor(buffered=True)
		
# format movie name
def formatName(title):
	searchstring = ""
	words = title.split()
	firstwordthe = False
	if words[0] == "The" or words[0] == "the":
		firstwordthe = True
	startindex = 0
	if firstwordthe:
		startindex = 1
	for word in words[startindex:]:
		searchstring += word + "-"
	searchstring = searchstring[:-1]
	if firstwordthe:
		searchstring += ",-The"
	
	return searchstring
			
		
		
# get movies
def getMovies():
	global GOODCOUNT
	global BADCOUNT
	global BADTITLES
	for title in MOVIES:
		try:
			url = "https://www.imsdb.com/scripts/{}.html".format(formatName(title))
			print(url)
			html = urllib.request.urlopen(url).read()
			soup = BeautifulSoup(html, "html.parser")
			script = soup.find("td", {"class" : "scrtext"}).text
			if len("".join(script.split())) < 150:
				print("NO SCRIPT FOR {}".format(title))
				BADTITLES.append(title)
				BADCOUNT += 1
				continue
			statement = """INSERT INTO NIH.Movies (Title, Text) VALUES ("{}", "{}")""".format(formatScript(title), formatScript(script))
			SQL_CURSOR.execute(statement)
			SQL_CONNECTION.commit()
			GOODCOUNT += 1
		except Exception as e:
			print("EXCEPTION in getting script {}: {}".format(title, e))
			BADTITLES.append(title)
			BADCOUNT += 1
			continue
			
###### MAIN SEQUENCE ######
init()
getMovies()
bf = open(BADFILE, "w+")
for title in BADTITLES:
	bf.write(title + "\n")
bf.close()
print("GOOD: {}".format(GOODCOUNT))
print("BAD: {}".format(BADCOUNT))