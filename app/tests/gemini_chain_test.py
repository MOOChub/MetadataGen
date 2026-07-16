from app.llm_support.deprecated.gemini_chain import execute_chain
from pprint import pprint

title = "Sustainability in the digital age: AI and Sustainability - Balancing Innovation and Responsibility"
description = '<h2>Welcome to the "Sustainability in the Digital Age" series</h2>\n\n<p>This ' \
              'course explores the critical&nbsp; intersection of AI and sustainability, highlighting ' \
              'how technological advancement can align with environmental responsibility. It offers ' \
              'insights into the dual nature of AI, noting its potential for increasing efficiency ' \
              'and driving sustainable innovation, while also acknowledging the significant energy ' \
              'consumption involved in training and applying AI models. In this course, we are not ' \
              'only examining the paradox of AI and sustainability but also provides actionable ' \
              'recommendations for incorporating sustainability into AI application development. By ' \
              "examining AI's transformative role and its environmental impact, the course offers a " \
              "comprehensive understanding of how AI can be harnessed to support global sustainability " \
              "goals effectively.</p>\n\n<hr>\n\n<p>This course is part of the <strong>Sustainability in " \
              "the Digital Age</strong> series, a collaborative project between colleagues from Stanford " \
              "University, SAP and the Hasso Plattner Institute. </p>\n"

pprint(execute_chain(title, description))
