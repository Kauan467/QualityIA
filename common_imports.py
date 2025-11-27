import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers # type: ignore
import os
import json
from datetime import datetime
import logging
from PIL import Image
from flask import Flask, render_template_string, request, jsonify, Response
import threading
import time
from pathlib import Path
import pandas as pd
import smtplib
import requests
from sklearn.model_selection import train_test_split
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)