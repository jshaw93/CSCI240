This file explains the differences between my ER Diagram and current iteration of my table examples.

Item:
  Added ItemRecipeID foreign key to connect the item to its Recipe

Skill:
  No longer connects to Item, but instead to Recipe

Recipe:
  Added ItemCreationID and SkillName foreign keys, Ingredients table created and linked via IngredientID

Player:
  Created new table Favorites to track favorited items in order to normalize to 1NF.

New tables:
  Favorites - Table of favorited item ids by FavoriteID
  Ingredients - Table of ingredient items as well as their quantity by IngredientID to normalize to 1NF.
