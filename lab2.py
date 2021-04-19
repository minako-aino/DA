import pandas as pd
from spyre import server
import matplotlib.pyplot as plt

class page(server.App):

    title = "Global Vegetation Health Products"

    inputs = [ {
                    "type":'checkboxgroup',
                    "label": 'Тип Даних',
                    "options" : [
                        {"label": "VCI ", "value":"vci"},
                        {"label": "TCI ", "value":"tci"},
                        {"label": "VHI ", "value":"vhi"}
                    ],
                    "key": 'vid',
                    "action_id" : "update_data",
                },
              { "type":'dropdown',
                    "label": 'Область',
                    "options" : [ {"label": "Vinnytsya ", "value":"24"},
                                  {"label": "Volyn ", "value":"26"},
                                  {"label": "Dnipro ", "value":"5"},
                                  {"label": "Donetsk ", "value":"6"},
                                  {"label": "Zhytomyr ", "value":"27"},
                                  {"label": "Transkarpathia ", "value":"23"},
                                  {"label": "Zaporyzhya ", "value":"26"},
                                  {"label": "Ivano-Frankivsk ", "value":"7"},
                                  {"label": "Kyiv ", "value":"11"},
                                  {"label": "Kyiv City ", "value":"12"},
                                  {"label": "Kropyvnytskyi ", "value":"13"},
                                  {"label": "Luhansk ", "value":"14"},
                                  {"label": "Lviv ", "value":"15"},
                                  {"label": "Mykolaiv ", "value":"16"},
                                  {"label": "Odessa ", "value":"17"},
                                  {"label": "Poltava ", "value":"18"},
                                  {"label": "Pivne ", "value":"19"},
                                  {"label": "Sumy ", "value":"21"},
                                  {"label": "Ternopil ", "value":"22"},
                                  {"label": "Kharkiv ", "value":"8"},
                                  {"label": "Kherson ", "value":"9"},
                                  {"label": "Khmelnytskyi ", "value":"10"},
                                  {"label": "Cherkasy ", "value":"1"},
                                  {"label": "Chernivtsi ", "value":"3"},
                                  {"label": "Chernihiv ", "value":"2"},
                                  {"label": "Crimea ", "value":"4"},
                                  {"label": "Sevastopol ", "value":"20"}],
                    "key": 'zone',
                    "action_id": "update_data"
                  },
                  {
                        "type":'slider',
                        "label": 'Year',
                        "min" : 1981,
                        "max" : 2021,
                        "key": 'year',
                        "action_id" : "update_data"
                    },
                    {
                        "type":'text',
                        "label": 'Weeks',
                        "value" : '1-52',
                        "key": 'time',
                        "action_id" : "update_data"
                    }]

    controls = [{   "type" : "button",
                    "label": 'Update',
                    "id" : "update_data"},
                {
                    "type" : "button",
                    "label": 'Download',
                    "id" : "dowld_file"
                }
                ]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot",
                    "on_page_load" : False},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True },
                    {
                    'type':'download',
                    "control_id" : "dowld_file",
                    'id':'results_csv',
                    'on_page_load': False
                }]

    def getData(self, params):
        new_index = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 26, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 27, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}
        head = ['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi']
        num = int(params['zone'])
        num = new_index[num]
        year = int(params['year'])

        time = params['time'].split("-")

        url=f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={num}&year1=1981&year2=2021&type=Mean'
        df = pd.read_csv(url ,index_col=None, header=1, names = head, usecols=head)
        df = df.drop(df.loc[df['vci'] == -1].index).dropna()
        df = df[df['year'] == str(year)]
        df = df.drop(df.loc[df['week'] < int(time[0])].index)
        df = df.drop(df.loc[df['week'] > int(time[1])].index)
        df['week'] = pd.to_numeric(df['week'], downcast='integer')
        self.dataframe = df
        return df

    def getPlot(self, params):
        vid = params['vid']
        df = self.getData(params)    
        
        plt.figure()
        if len(vid) == 0:
            plt_obj = plt.text(0.5, 0.5, 'Choose Data!',  dict(size=25),horizontalalignment='center')
            fig = plt_obj.get_figure()
            return fig
        else:
            plt_obj = df.plot(y=vid, x='week', kind="bar", figsize=(30, 13), fontsize = 14, grid = True)
            plt_obj.legend(fontsize = 15)
            plt_obj.set_ylabel("Value", fontsize = 14)
            plt.xlabel("Week", fontsize = 14)
            fig = plt_obj.get_figure()
            return fig
        
app = page()
app.launch(port=9903)
