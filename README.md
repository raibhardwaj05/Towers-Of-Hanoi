# Towers Of Hanoi Game 🏰

An interactive Python implementation of the classic Towers of Hanoi puzzle — featuring a graphical UI (Tkinter), animated moves (Turtle), and persistent storage using MySQL.

## Table of Contents
- [About](#about)  
- [Features](#features)  
- [Architecture & Design](#architecture--design)  
- [Demo / Screenshots](#demo--screenshots)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
  - [Running the Game](#running-the-game)  
- [How It Works](#how-it-works)  
- [Project Structure](#project-structure)  
- [Technologies Used](#technologies-used)  
- [Acknowledgements](#acknowledgements)

---

## About  
The Towers Of Hanoi game lets players solve the famous recursive puzzle — move a stack of disks from one rod to another under specific constraints.  
This implementation enhances the experience with:  
- A **Tkinter GUI** for user inputs and controls  
- A **Turtle Graphics** module to animate disk movements  
- A **MySQL database backend** to store player profiles, move counts, timers, and leaderboard data  
- Designed and developed in **PyCharm IDE**  

This project is ideal for learning algorithmic thinking, GUI programming, database integration, and object-oriented design in Python.

---

## Features  
- Select the number of disks (difficulty) & play manually or use auto-solve mode  
- Animated disk moves (Turtle) showing each step  
- Move counter and timer display  
- Prevents invalid moves (e.g., placing larger disk on smaller)  
- Player profile creation and login  
- Persistent storage of game sessions in MySQL; save/load feature  
- Leaderboard display of best times/moves  
- Modular codebase – easy to extend (e.g., theme support, more rods)  

---
 
