# imports
from flask import Flask, redirect, url_for,render_template, request,flash
import smtplib
from email.message import EmailMessage
import sqlite3
import calendar
import random
import datetime
import threading
import time

# app setup