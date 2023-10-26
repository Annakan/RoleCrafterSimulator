from simulators.cards import CardTemplate

# Materia templates

materia_card_template_L1 = CardTemplate(t="materia_L1", c=40)
materia_card_template_L2 = CardTemplate(t="materia_L2", c=50)
materia_card_template_L3 = CardTemplate(t="materia_L3", c=70)
materia_card_template_L4 = CardTemplate(t="materia_L4", c=90)
materia_card_template_L5 = CardTemplate(t="materia_L5", c=100)

# Main product templates
product_card_template_L1 = CardTemplate(t="product_L1", c=40)
product_card_template_L2 = CardTemplate(t="product_L2", c=50)
product_card_template_L3 = CardTemplate(t="product_L3", c=60)
product_card_template_L4 = CardTemplate(t="product_L4", c=70)
product_card_template_L5 = CardTemplate(t="product_L5", c=80)
product_card_template_L6 = CardTemplate(t="product_L6", c=90)
product_card_template_L7 = CardTemplate(t="product_L6", c=100)

# default templates

default_card_template_L1 = CardTemplate(t="default_L1", c=40, d=40)
default_card_template_L2 = CardTemplate(t="default_L2", c=50, d=50)
default_card_template_L3 = CardTemplate(t="default_L3", c=70, d=70)
default_card_template_L4 = CardTemplate(t="default_L4", c=90, d=90)
default_card_template_L5 = CardTemplate(t="default_L5", c=100, d=100)


tool_card_template = CardTemplate(t="IrremovableTool", c=40, d=40, _fixed=True) # cette carte ne peut pas être retirée (C=1000)
