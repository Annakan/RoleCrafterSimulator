from simulators import CARD_TOOL, CARD_DEFAULT, CARD_PRODUCT, CARD_MATERIA
from simulators.cards import CardTemplate

# Materia templates

materia_card_template_40 = CardTemplate(t=CARD_MATERIA, l=1, c=40, _fixed=True)
materia_card_template_50 = CardTemplate(t=CARD_MATERIA, l=2, c=50, _fixed=True)
materia_card_template_60 = CardTemplate(t=CARD_MATERIA, l=2, c=60, _fixed=True)
materia_card_template_70 = CardTemplate(t=CARD_MATERIA, l=3, c=70, _fixed=True)
materia_card_template_90 = CardTemplate(t=CARD_MATERIA, l=4, c=90, _fixed=True)
materia_card_template_L5 = CardTemplate(t=CARD_MATERIA, l=5, c=100, _fixed=True)

# Main product templates
product_card_template_40 = CardTemplate(t=CARD_PRODUCT, l=1, c=40, _fixed=True)
product_card_template_50 = CardTemplate(t=CARD_PRODUCT, l=2, c=50, _fixed=True)
product_card_template_60 = CardTemplate(t=CARD_PRODUCT, l=3, c=60, _fixed=True)
product_card_template_70 = CardTemplate(t=CARD_PRODUCT, l=4, c=70, _fixed=True)
product_card_template_80 = CardTemplate(t=CARD_PRODUCT, l=5, c=80, _fixed=True)
product_card_template_90 = CardTemplate(t=CARD_PRODUCT, l=6, c=90, _fixed=True)
product_card_template_100 = CardTemplate(t=CARD_PRODUCT, l=6, c=100, _fixed=True)

# default templates

default_card_template_40 = CardTemplate(t=CARD_DEFAULT, l=1, c=40, d=40)
default_card_template_50 = CardTemplate(t=CARD_DEFAULT, l=2, c=50, d=50)
default_card_template_60 = CardTemplate(t=CARD_DEFAULT, l=2, c=60, d=60)
default_card_template_70 = CardTemplate(t=CARD_DEFAULT, l=3, c=70, d=70)
default_card_template_80 = CardTemplate(t=CARD_DEFAULT, l=3, c=80, d=80)
default_card_template_90 = CardTemplate(t=CARD_DEFAULT, l=4, c=90, d=90)
default_card_template_100 = CardTemplate(t=CARD_DEFAULT, l=5, c=100, d=100)
default_card_template_110 = CardTemplate(t=CARD_DEFAULT, l=5, c=100, d=110)
default_card_template_120 = CardTemplate(t=CARD_DEFAULT, l=5, c=100, d=120)

tool_card_template = CardTemplate(t=CARD_TOOL, l=1, c=40, d=40,
                                  _fixed=True)  # cette carte ne peut pas être retirée (C=1000)
