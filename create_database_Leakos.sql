-- MySQL Workbench Foexercisesrward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema ProjectPYDB delete if already existing
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `ProjectPYDB`;
-- -----------------------------------------------------
-- Schema ProjectPYDB
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `ProjectPYDB` DEFAULT CHARACTER SET utf8 ;
USE `ProjectPYDB` ;

-- -----------------------------------------------------
-- Table `ProjectPYDB`.`students`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjectPYDB`.`students` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nickname` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `nickname_UNIQUE` (`nickname` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ProjectPYDB`.`exercises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjectPYDB`.`exercises` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ProjectPYDB`.`students_has_exercises`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ProjectPYDB`.`students_has_exercises` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `try` INT NOT NULL,
  `success` INT NOT NULL,
  `chronometer` TIME NOT NULL,
  `start_date_and_time` DATETIME NOT NULL,
  `student_id` INT NOT NULL,
  `exercise_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_students_has_exercises_students1_idx` (`student_id` ASC) VISIBLE,
  INDEX `fk_students_has_exercises_exercises1_idx` (`exercise_id` ASC) VISIBLE,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  CONSTRAINT `fk_students_has_exercises_students1`
    FOREIGN KEY (`student_id`)
    REFERENCES `ProjectPYDB`.`students` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_students_has_exercises_exercises1`
    FOREIGN KEY (`exercise_id`)
    REFERENCES `ProjectPYDB`.`exercises` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;