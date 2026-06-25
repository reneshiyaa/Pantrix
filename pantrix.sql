-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: pantrix
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `favorites`
--

DROP TABLE IF EXISTS `favorites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favorites` (
  `favorite_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `recipe_id` int DEFAULT NULL,
  PRIMARY KEY (`favorite_id`),
  KEY `user_id` (`user_id`),
  KEY `recipe_id` (`recipe_id`),
  CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favorites`
--

LOCK TABLES `favorites` WRITE;
/*!40000 ALTER TABLE `favorites` DISABLE KEYS */;
INSERT INTO `favorites` VALUES (1,2,1),(2,2,20),(3,2,12);
/*!40000 ALTER TABLE `favorites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredient_substitutes`
--

DROP TABLE IF EXISTS `ingredient_substitutes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredient_substitutes` (
  `ingredient_id` int NOT NULL,
  `substitute_id` int NOT NULL,
  PRIMARY KEY (`ingredient_id`,`substitute_id`),
  KEY `substitute_id` (`substitute_id`),
  CONSTRAINT `ingredient_substitutes_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`),
  CONSTRAINT `ingredient_substitutes_ibfk_2` FOREIGN KEY (`substitute_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredient_substitutes`
--

LOCK TABLES `ingredient_substitutes` WRITE;
/*!40000 ALTER TABLE `ingredient_substitutes` DISABLE KEYS */;
INSERT INTO `ingredient_substitutes` VALUES (72,12),(13,14),(16,15),(15,16),(18,19),(44,39),(63,40),(42,41),(41,42),(39,44),(60,59),(61,59),(59,60),(40,63);
/*!40000 ALTER TABLE `ingredient_substitutes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `ingredient_id` int NOT NULL AUTO_INCREMENT,
  `ingredient_name` varchar(100) NOT NULL,
  PRIMARY KEY (`ingredient_id`),
  UNIQUE KEY `ingredient_name` (`ingredient_name`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (84,'Almonds'),(89,'Apple'),(99,'Baking Powder'),(100,'Baking Soda'),(88,'Banana'),(2,'Basmati Rice'),(81,'Bay Leaf'),(28,'Beans'),(9,'Beetroot'),(57,'Besan'),(70,'Black Pepper'),(45,'Bread'),(30,'Brinjal'),(23,'Broccoli'),(3,'Brown Rice'),(46,'Burger Bun'),(40,'Butter'),(21,'Cabbage'),(10,'Capsicum'),(78,'Cardamom'),(8,'Carrot'),(83,'Cashew Nuts'),(22,'Cauliflower'),(41,'Cheese'),(33,'Chicken'),(67,'Chilli Sauce'),(96,'Chocolate'),(80,'Cinnamon'),(79,'Cloves'),(97,'Cocoa Powder'),(15,'Coriander Leaves'),(73,'Coriander Powder'),(52,'Cornflakes'),(37,'Crab'),(43,'Cream'),(20,'Cucumber'),(75,'Cumin Seeds'),(39,'Curd'),(17,'Curry Leaves'),(87,'Dates'),(31,'Drumstick'),(4,'Egg'),(77,'Fennel Seeds'),(35,'Fish'),(53,'Flour'),(74,'Garam Masala'),(13,'Garlic'),(63,'Ghee'),(14,'Ginger'),(94,'Grapes'),(11,'Green Chilli'),(61,'Honey'),(60,'Jaggery'),(18,'Lemon'),(19,'Lime'),(55,'Maida'),(91,'Mango'),(68,'Mayonnaise'),(38,'Milk'),(16,'Mint Leaves'),(25,'Mushroom'),(69,'Mustard Sauce'),(76,'Mustard Seeds'),(34,'Mutton'),(49,'Noodles'),(51,'Oats'),(62,'Oil'),(5,'Onion'),(90,'Orange'),(42,'Paneer'),(48,'Pasta'),(26,'Peas'),(92,'Pineapple'),(47,'Pizza Base'),(7,'Potato'),(36,'Prawns'),(29,'Pumpkin'),(32,'Radish'),(86,'Raisins'),(56,'Rava'),(12,'Red Chilli'),(72,'Red Chilli Powder'),(1,'Rice'),(58,'Salt'),(65,'Soy Sauce'),(24,'Spinach'),(82,'Star Anise'),(95,'Strawberry'),(59,'Sugar'),(27,'Sweet Corn'),(6,'Tomato'),(66,'Tomato Ketchup'),(71,'Turmeric Powder'),(98,'Vanilla Essence'),(50,'Vermicelli'),(64,'Vinegar'),(85,'Walnuts'),(93,'Watermelon'),(54,'Wheat Flour'),(44,'Yogurt');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pantry`
--

DROP TABLE IF EXISTS `pantry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pantry` (
  `pantry_id` int NOT NULL AUTO_INCREMENT,
  `ingredient_id` int DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`pantry_id`),
  KEY `ingredient_id` (`ingredient_id`),
  KEY `fk_pantry_user` (`user_id`),
  CONSTRAINT `fk_pantry_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `pantry_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pantry`
--

LOCK TABLES `pantry` WRITE;
/*!40000 ALTER TABLE `pantry` DISABLE KEYS */;
INSERT INTO `pantry` VALUES (63,2,NULL,2),(64,10,NULL,2),(65,21,NULL,2),(66,75,NULL,2),(67,11,NULL,2),(68,13,NULL,2),(69,26,NULL,2),(70,71,NULL,2);
/*!40000 ALTER TABLE `pantry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_ingredients`
--

DROP TABLE IF EXISTS `recipe_ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_ingredients` (
  `recipe_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`recipe_id`,`ingredient_id`),
  KEY `ingredient_id` (`ingredient_id`),
  CONSTRAINT `recipe_ingredients_ibfk_1` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`recipe_id`),
  CONSTRAINT `recipe_ingredients_ibfk_2` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_ingredients`
--

LOCK TABLES `recipe_ingredients` WRITE;
/*!40000 ALTER TABLE `recipe_ingredients` DISABLE KEYS */;
INSERT INTO `recipe_ingredients` VALUES (1,1,'1 cup'),(1,4,'2'),(1,5,'1'),(1,13,'2 cloves'),(2,1,'1 cup'),(2,5,'1'),(2,6,'2'),(2,58,'to taste'),(2,72,'1 tsp'),(3,1,'1 cup'),(3,18,'1'),(3,58,'to taste'),(3,76,'1 tsp'),(4,1,'1 cup'),(4,5,'1'),(4,8,'1'),(4,10,'1'),(4,26,'1/2 cup'),(4,62,'1 tbsp'),(5,1,'1 cup'),(5,5,'1'),(5,13,'2 cloves'),(5,42,'100g'),(5,62,'1 tbsp'),(6,13,'4 cloves'),(6,40,'2 tbsp'),(6,45,'4 slices'),(7,41,'2 slices'),(7,45,'2 slices'),(7,67,'1 tbsp'),(8,5,'1'),(8,6,'1'),(8,20,'1/2'),(8,45,'2 slices'),(8,67,'1 tbsp'),(9,4,'2'),(9,38,'1/4 cup'),(9,45,'2 slices'),(9,59,'1 tsp'),(10,4,'2'),(10,5,'1'),(10,58,'to taste'),(10,62,'1 tsp'),(11,4,'3'),(11,40,'1 tbsp'),(11,58,'to taste'),(11,70,'1 tsp'),(12,8,'1'),(12,10,'1'),(12,26,'1/2 cup'),(12,49,'200g'),(12,64,'1 tbsp'),(13,5,'1'),(13,13,'2 cloves'),(13,33,'150g'),(13,49,'200g'),(13,64,'1 tbsp'),(14,5,'1'),(14,6,'2'),(14,48,'200g'),(14,62,'1 tbsp'),(14,74,'1 tsp'),(15,38,'1 cup'),(15,40,'1 tbsp'),(15,41,'50g'),(15,48,'200g'),(15,58,'to taste'),(16,5,'1'),(16,7,'1'),(16,8,'1'),(16,24,'1 cup'),(16,58,'to taste'),(17,5,'1'),(17,8,'1'),(17,27,'1 cup'),(17,58,'to taste'),(18,85,'1'),(18,86,'1'),(18,87,'1'),(18,88,'1'),(19,4,'1'),(19,38,'1 cup'),(19,53,'1 cup'),(19,59,'2 tbsp'),(19,95,'1 tsp'),(20,6,'2'),(20,10,'1'),(20,41,'100 g'),(20,47,'1'),(20,67,'2 tbsp');
/*!40000 ALTER TABLE `recipe_ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `recipe_id` int NOT NULL AUTO_INCREMENT,
  `recipe_name` varchar(100) NOT NULL,
  `cooking_time` int DEFAULT NULL,
  `difficulty` varchar(20) DEFAULT NULL,
  `instructions` text,
  PRIMARY KEY (`recipe_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES (1,'Egg Fried Rice',20,'Easy','Step 1: Cook 1 cup rice and spread it on a plate to cool completely.\nStep 2: Heat 1 tbsp oil in a wok over high heat until smoking hot.\nStep 3: Crack in 2 eggs, scramble 30 seconds until just set, push to one side.\nStep 4: Add chopped onion and minced garlic to the empty side. Stir-fry 1-2 minutes.\nStep 5: Add the cooled rice and break up any clumps.\nStep 6: Toss everything together over high heat.\nStep 7: Season with soy sauce, salt, and black pepper. Stir-fry 2-3 minutes.\nStep 8: Garnish with spring onions and serve hot.'),(2,'Tomato Rice',25,'Easy','Step 1: Wash 1 cup rice and soak 15 minutes. Drain and set aside.\nStep 2: Heat 2 tbsp oil, add mustard seeds, let them splutter.\nStep 3: Add curry leaves, green chilli, and chopped onion. Saute 3-4 minutes.\nStep 4: Add chopped tomatoes, turmeric, chilli powder, and salt. Mix well.\nStep 5: Cook 6-8 minutes until tomatoes break down and oil separates.\nStep 6: Add the drained rice and stir to coat every grain.\nStep 7: Pour in 2 cups hot water and bring to a boil, then reduce heat to low.\nStep 8: Cover and cook 15 minutes, rest 5 minutes, fluff, and serve.'),(3,'Lemon Rice',15,'Easy','Step 1: Cook 1 cup rice until fluffy and let it cool completely.\nStep 2: Heat 2 tbsp oil, add mustard seeds, let them splutter.\nStep 3: Add chana dal and urad dal if available, fry 1 minute until golden.\nStep 4: Add dried red chilli, green chilli, and curry leaves. Fry 30 seconds.\nStep 5: Add a pinch of turmeric powder and stir once.\nStep 6: Add the cooled rice and mix gently from the bottom.\nStep 7: Squeeze in juice of 1 lemon, add salt, toss gently 2 minutes.\nStep 8: Garnish with peanuts and coriander leaves and serve.'),(4,'Vegetable Fried Rice',25,'Easy','Step 1: Cook 1 cup rice and let it cool completely.\nStep 2: Dice carrot, capsicum, and onion finely. Keep peas ready.\nStep 3: Heat 1 tbsp oil in a wok on the highest heat.\nStep 4: Add minced garlic, stir 20 seconds, then add onion, cook 1 minute.\nStep 5: Add carrot first, then capsicum and peas. Stir-fry 3-4 minutes.\nStep 6: Add the cold rice, break up lumps, toss with vegetables.\nStep 7: Add soy sauce, salt, and black pepper. Stir-fry 2-3 minutes.\nStep 8: Serve immediately, garnished with spring onion greens.'),(5,'Paneer Fried Rice',25,'Medium','Step 1: Cook 1 cup basmati rice until fluffy and cool completely.\nStep 2: Cut 100g paneer into cubes, pan-fry in 1 tsp oil until golden, set aside.\nStep 3: Heat remaining oil on high heat, add minced garlic, fry 30 seconds.\nStep 4: Add sliced onion and stir-fry 2 minutes until edges brown.\nStep 5: Add the cooled rice, toss on high flame, breaking all clumps.\nStep 6: Add soy sauce, salt, and black pepper, mix thoroughly.\nStep 7: Gently fold in paneer cubes, stirring only 2-3 times.\nStep 8: Garnish with spring onions and serve hot immediately.'),(6,'Garlic Bread',15,'Easy','Step 1: Preheat oven to 180C. \nStep 2: Mince garlic. \nStep 3: Mix butter with garlic and salt. \nStep 4: Slice bread. \nStep 5: Spread garlic butter. \nStep 6: Place on tray. \nStep 7: Bake 8 min covered then 5 min uncovered. \nStep 8: Serve immediately.'),(7,'Cheese Sandwich',10,'Easy','Step 1: Take 2 slices of bread and lightly butter one side of each.\nStep 2: Place sliced or grated cheese on the unbuttered side of one slice.\nStep 3: Optionally add tomato, dried herbs, and black pepper on top.\nStep 4: Close the sandwich, buttered side facing outward on both sides.\nStep 5: Heat a non-stick pan on medium heat. No extra oil needed.\nStep 6: Place the sandwich on the pan and press with a spatula.\nStep 7: Cook 2-3 minutes until golden, flip, cook 2 minutes until cheese melts.\nStep 8: Cut diagonally and serve immediately with ketchup or chutney.'),(8,'Vegetable Sandwich',15,'Easy','Step 1: Slice cucumber, tomato, and onion thinly. Pat dry with a paper towel.\nStep 2: Mix mayonnaise or chutney with black pepper and chaat masala.\nStep 3: Lightly toast the bread slices until just golden.\nStep 4: Spread the sauce mixture on one side of both slices.\nStep 5: Layer cucumber, tomato, then onion rings on one slice.\nStep 6: Sprinkle chaat masala and salt. Add green chilli if desired.\nStep 7: Place second slice on top, spread side down, press gently.\nStep 8: Slice diagonally and serve fresh immediately.'),(9,'French Toast',15,'Easy','Step 1: Crack 2 eggs into a wide, shallow bowl.\nStep 2: Add 1/4 cup milk, 1 tsp sugar, a pinch of cinnamon and salt. Whisk smooth.\nStep 3: Heat a pan on medium heat and melt 1 tsp butter.\nStep 4: Dip a bread slice in the egg mixture, soaking 10 seconds each side.\nStep 5: Place the soaked slice in the buttered pan.\nStep 6: Cook undisturbed 2-3 minutes until deep golden.\nStep 7: Flip and cook the second side 2 minutes until golden.\nStep 8: Serve warm, dusted with sugar and drizzled with honey.'),(10,'Omelette',10,'Easy','Step 1: Crack 2-3 eggs into a bowl with salt, pepper, and 1 tbsp water or milk.\nStep 2: Beat the eggs for 30 seconds until fully combined.\nStep 3: Finely chop onion, green chilli, and coriander leaves.\nStep 4: Heat a pan on medium-high with 1 tsp oil or butter.\nStep 5: Add onion and chilli, saute 30-45 seconds.\nStep 6: Pour in the egg and tilt the pan to spread it evenly.\nStep 7: Let edges set 30 seconds, sprinkle coriander on top.\nStep 8: Fold one half over the other and serve immediately.'),(11,'Scrambled Eggs',10,'Easy','Step 1: Crack 3 eggs into a bowl with 1 tbsp milk, salt, and pepper. Whisk well.\nStep 2: Place a non-stick pan on low heat.\nStep 3: Add 1 tbsp butter and let it melt slowly on low heat.\nStep 4: Pour in the eggs and leave undisturbed 20-30 seconds.\nStep 5: Slowly fold the eggs from the edges toward the centre.\nStep 6: Continue folding every 20-30 seconds until soft curds form.\nStep 7: Remove from heat when about 90 percent set but still glossy.\nStep 8: Season and serve immediately on buttered toast.'),(12,'Vegetable Noodles',20,'Easy','Step 1: Boil noodles 1 minute less than packet instructions.\nStep 2: Drain, rinse under cold water, toss with a few drops of oil.\nStep 3: Julienne carrot, slice capsicum, shred cabbage, chop spring onions.\nStep 4: Heat 1 tbsp oil in a wok on the highest heat.\nStep 5: Add garlic, fry 20 seconds, add carrot and capsicum, stir-fry 2 minutes.\nStep 6: Add cabbage and spring onion whites, toss 2 more minutes.\nStep 7: Add noodles, soy sauce, chilli sauce, salt, and pepper. Stir-fry 2 minutes.\nStep 8: Plate immediately, garnished with spring onion greens.'),(13,'Chicken Noodles',25,'Medium','Step 1: Slice 150g chicken breast into thin strips.\nStep 2: Marinate with 1 tsp soy sauce, pepper, and 1/2 tsp cornflour for 15 minutes.\nStep 3: Boil noodles until al dente, drain, rinse, and toss with oil.\nStep 4: Heat oil on high heat, add garlic and ginger, stir 30 seconds.\nStep 5: Add chicken, sear 2 minutes, then toss and cook 2-3 more minutes.\nStep 6: Add sliced onion and capsicum, stir-fry 2 minutes.\nStep 7: Add noodles, soy sauce, chilli sauce, salt. Stir-fry 2 minutes.\nStep 8: Garnish with spring onions and serve immediately.'),(14,'Masala Pasta',25,'Easy','Step 1: Boil pasta until al dente, reserve 1/4 cup pasta water, drain.\nStep 2: Heat 1 tbsp oil, cook chopped onion on medium heat 5-6 minutes.\nStep 3: Add minced garlic, cook 1-2 minutes.\nStep 4: Add chopped tomatoes, cook 3 minutes, add turmeric, chilli powder, coriander powder, salt.\nStep 5: Cook the masala 6-8 minutes until tomatoes break down.\nStep 6: Add diced capsicum, cook 2 minutes, keeping it crunchy.\nStep 7: Add the pasta and toss well, adding reserved water if too thick.\nStep 8: Finish with garam masala and coriander leaves. Serve hot.'),(15,'White Sauce Pasta',30,'Medium','Step 1: Cook pasta until al dente, reserve 1/2 cup pasta water, drain.\nStep 2: Melt 2 tbsp butter in a saucepan on medium heat.\nStep 3: Add 2 tbsp flour and whisk 1-2 minutes to form a roux.\nStep 4: Reduce heat, gradually whisk in 1 cup milk until smooth.\nStep 5: Whisk continuously as it thickens, about 5-7 minutes.\nStep 6: Season with salt, white pepper, and a pinch of nutmeg.\nStep 7: Stir in 50g grated cheese, then add pasta and toss to coat.\nStep 8: Thin with reserved water if needed. Plate and garnish.'),(16,'Vegetable Soup',20,'Easy','Step 1: Chop carrot, potato, onion, and spinach into small cubes.\nStep 2: Heat 1 tbsp oil or butter in a pot with a bay leaf.\nStep 3: Add onion and garlic, saute 3-4 minutes until soft.\nStep 4: Add carrot and potato, cook 2 minutes.\nStep 5: Pour in 3-4 cups stock or water with salt and pepper, bring to a boil.\nStep 6: Reduce heat, cover, simmer 18-20 minutes until tender.\nStep 7: Add spinach in the last 2 minutes of cooking.\nStep 8: Blend half for a creamier texture if desired and serve hot.'),(17,'Sweet Corn Soup',20,'Easy','Cook corn and vegetables in broth.'),(18,'Fruit Salad',10,'Easy','Step 1: Wash all fruits thoroughly under cold running water.\nStep 2: Chop banana into rounds, dice apple, segment orange removing seeds.\nStep 3: Cube mango if using. Halve grapes and remove seeds.\nStep 4: Toss apple and banana with lemon juice right away to prevent browning.\nStep 5: Place all the cut fruit into a large mixing bowl.\nStep 6: Squeeze in juice of half a lemon, add honey and chaat masala.\nStep 7: Toss gently with two spoons so every piece is coated.\nStep 8: Refrigerate at least 15-20 minutes before serving cold.'),(19,'Pancakes',20,'Easy','Step 1: Sift together 1 cup flour, 1 tsp baking powder, 2 tbsp sugar, and salt.\nStep 2: Whisk 1 egg, 1 cup milk, and 2 tbsp melted butter until smooth.\nStep 3: Pour wet into dry ingredients, stir gently until just combined.\nStep 4: Let the batter rest 5 minutes without touching it.\nStep 5: Heat a pan on medium-low heat, lightly greased with butter.\nStep 6: Pour 1/4 cup batter onto the centre of the pan.\nStep 7: Cook until bubbles form, about 2 minutes, flip, cook 1-2 more minutes.\nStep 8: Serve immediately with syrup, honey, or fruit.'),(20,'Pizza',40,'Hard','Step 1: Preheat oven to its highest setting, ideally 220-250C.\nStep 2: Spread sauce evenly on the base, leaving a border for the crust.\nStep 3: Sprinkle a base layer of shredded mozzarella over the sauce.\nStep 4: Add toppings like capsicum, onion, and tomato, evenly distributed.\nStep 5: Add a final generous layer of cheese over the toppings.\nStep 6: Slide the pizza onto a preheated hot tray in the oven.\nStep 7: Bake 12-15 minutes until cheese is bubbling and golden.\nStep 8: Rest 2-3 minutes, slice into wedges, and serve immediately.');
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopping_list`
--

DROP TABLE IF EXISTS `shopping_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shopping_list` (
  `shopping_id` int NOT NULL AUTO_INCREMENT,
  `ingredient_id` int DEFAULT NULL,
  `quantity` varchar(50) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`shopping_id`),
  KEY `ingredient_id` (`ingredient_id`),
  KEY `fk_sl_user` (`user_id`),
  CONSTRAINT `fk_sl_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  CONSTRAINT `shopping_list_ibfk_1` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`ingredient_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopping_list`
--

LOCK TABLES `shopping_list` WRITE;
/*!40000 ALTER TABLE `shopping_list` DISABLE KEYS */;
INSERT INTO `shopping_list` VALUES (1,13,'2 cloves',NULL),(3,6,'2',2),(4,10,'1',2),(5,41,'100 g',2),(6,67,'2 tbsp',2),(7,47,'1',2),(8,38,'1 cup',2),(9,95,'1 tsp',2),(10,45,'4 slices',2),(11,13,'4 cloves',2),(12,8,'1',2),(13,49,'200g',2),(14,64,'1 tbsp',2);
/*!40000 ALTER TABLE `shopping_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'Rene','Reneshiyaa@gmail.com','Rene@2007'),(3,'hjhjj','jjjjjjjjjju','Rene@2007');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-06-25 20:45:35
