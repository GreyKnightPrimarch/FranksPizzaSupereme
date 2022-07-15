-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema PizzaF
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema PizzaF
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `PizzaF` DEFAULT CHARACTER SET utf8 ;
USE `PizzaF` ;

-- -----------------------------------------------------
-- Table `PizzaF`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`User` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`User` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `FirstName` VARCHAR(255) NULL,
  `LastName` VARCHAR(255) NULL,
  `PassWordHash` VARCHAR(255) NULL,
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `Email` VARCHAR(255) NOT NULL,
  `Address` VARCHAR(255) NULL,
  `City` VARCHAR(255) NULL,
  `State` VARCHAR(255) NULL,
  `ZIP` VARCHAR(20) NULL,
  PRIMARY KEY (`ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`CrustTypes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`CrustTypes` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`CrustTypes` (
  `CrustID` INT NOT NULL AUTO_INCREMENT,
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `Name` VARCHAR(255) NULL,
  `Description` VARCHAR(255) NULL,
  `Type` VARCHAR(45) NULL,
  `baseprice` DOUBLE NULL,
  PRIMARY KEY (`CrustID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`Sizes`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`Sizes` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`Sizes` (
  `SizeID` INT NOT NULL AUTO_INCREMENT,
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `Name` VARCHAR(255) NULL,
  `Description` VARCHAR(255) NULL,
  `Diameter` DOUBLE NULL,
  PRIMARY KEY (`SizeID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`Ingredient`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`Ingredient` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`Ingredient` (
  `IngredientID` INT NOT NULL AUTO_INCREMENT,
  `Name` VARCHAR(45) NULL,
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `Description` TEXT NULL,
  `Type` VARCHAR(45) NULL,
  `baseprice` DOUBLE NULL,
  PRIMARY KEY (`IngredientID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`PizzaIngredients`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`PizzaIngredients` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`PizzaIngredients` (
  `CombinationID` INT NOT NULL,
  `Pi_IngredientID` INT NOT NULL,
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  INDEX `fk_PizzaIngredients_Ingredients1_idx` (`Pi_IngredientID` ASC) VISIBLE,
  PRIMARY KEY (`CombinationID`),
  CONSTRAINT `fk_PizzaIngredients_Ingredients1`
    FOREIGN KEY (`Pi_IngredientID`)
    REFERENCES `PizzaF`.`Ingredient` (`IngredientID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`Pizza`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`Pizza` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`Pizza` (
  `PizzaID` INT NOT NULL,
  `UpdatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `Description` TEXT NULL,
  `Crust_ID` INT NOT NULL,
  `Size_ID` INT NOT NULL,
  `Pi_CombinationID` INT NOT NULL,
  `Name` VARCHAR(255) NULL,
  PRIMARY KEY (`PizzaID`),
  INDEX `fk_Pizza_CrustTypes1_idx` (`Crust_ID` ASC) VISIBLE,
  INDEX `fk_Pizza_Sizes1_idx` (`Size_ID` ASC) VISIBLE,
  INDEX `fk_Pizza_PizzaIngredients1_idx` (`Pi_CombinationID` ASC) VISIBLE,
  CONSTRAINT `fk_Pizza_CrustTypes1`
    FOREIGN KEY (`Crust_ID`)
    REFERENCES `PizzaF`.`CrustTypes` (`CrustID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pizza_Sizes1`
    FOREIGN KEY (`Size_ID`)
    REFERENCES `PizzaF`.`Sizes` (`SizeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Pizza_PizzaIngredients1`
    FOREIGN KEY (`Pi_CombinationID`)
    REFERENCES `PizzaF`.`PizzaIngredients` (`CombinationID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`FavoritePizzas`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`FavoritePizzas` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`FavoritePizzas` (
  `LikeID` INT NOT NULL,
  `CreatedAt` DATETIME NULL DEFAULT CURRENT_TIMESTAMP(),
  `UpdatedAt` DATETIME NULL DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
  `User_ID` INT NOT NULL,
  `Pizza_ID` INT NOT NULL,
  PRIMARY KEY (`LikeID`, `User_ID`),
  INDEX `fk_table1_User_idx` (`User_ID` ASC) VISIBLE,
  INDEX `fk_table1_Pizza_idx` (`Pizza_ID` ASC) VISIBLE,
  CONSTRAINT `fk_table1_User`
    FOREIGN KEY (`User_ID`)
    REFERENCES `PizzaF`.`User` (`ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_table1_Pizza`
    FOREIGN KEY (`Pizza_ID`)
    REFERENCES `PizzaF`.`Pizza` (`PizzaID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `PizzaF`.`PastOrder`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `PizzaF`.`PastOrder` ;

CREATE TABLE IF NOT EXISTS `PizzaF`.`PastOrder` (
  `OrderID` INT NOT NULL AUTO_INCREMENT,
  `Pizza_ID` INT NOT NULL,
  `CreatedAt` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`OrderID`),
  INDEX `fk_PastOrder_Pizza1_idx` (`Pizza_ID` ASC) VISIBLE,
  CONSTRAINT `fk_PastOrder_Pizza1`
    FOREIGN KEY (`Pizza_ID`)
    REFERENCES `PizzaF`.`Pizza` (`PizzaID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
