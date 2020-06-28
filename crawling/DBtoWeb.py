from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
import requests
from bs4 import BeautifulSoup
import dbModule

