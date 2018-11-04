import numpy as np
import pandas as pd
from backend.EnvironmentConfigurations import CAPITAL_ONE_API_KEY
import requests

r = requests.post(f"http://api.reimaginebanking.com/customers?key={CAPITAL_ONE_API_KEY}",
                  data =
                      {

                      }
                  )
