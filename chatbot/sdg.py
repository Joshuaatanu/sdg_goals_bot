class SDGManager:
    def __init__(self):
        self.sdg_responses = self._load_sdg_responses()

    def _load_sdg_responses(self):
        return {
            1: "SDG 1: No Poverty - Promote inclusive economic policies and living wages.",
            2: "SDG 2: Zero Hunger - Support sustainable agriculture and reduce food waste.",
            3: "SDG 3: Good Health - Implement workplace wellness programs and safety measures.",
            4: "SDG 4: Quality Education - Provide employee training on sustainability practices.",
            5: "SDG 5: Gender Equality - Ensure equal pay and leadership opportunities.",
            6: "SDG 6: Clean Water - Reduce water consumption and prevent pollution.",
            7: "SDG 7: Affordable Energy - Transition to renewable energy sources.",
            8: "SDG 8: Decent Work - Maintain ethical labor practices throughout supply chains.",
            9: "SDG 9: Innovation - Invest in sustainable technologies and infrastructure.",
            10: "SDG 10: Reduced Inequality - Promote diversity and inclusion initiatives.",
            11: "SDG 11: Sustainable Cities - Optimize logistics and reduce urban pollution.",
            12: "SDG 12: Responsible Consumption - Implement recycling and circular economy models.",
            13: "SDG 13: Climate Action - Measure carbon footprint and set reduction targets.",
            14: "SDG 14: Life Below Water - Reduce plastic use and prevent ocean pollution.",
            15: "SDG 15: Life on Land - Source materials sustainably and protect ecosystems.",
            16: "SDG 16: Peace and Justice - Ensure ethical governance and anti-corruption measures.",
            17: "SDG 17: Partnerships - Collaborate with NGOs and government organizations."
        }

    def get_sdg_info(self, sdg_number):
        return self.sdg_responses.get(sdg_number, "Please specify a valid SDG number (1-17).") 