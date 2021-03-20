from datetime import datetime, timedelta

import google.cloud.logging
import BenderBot

class CloudLogging:

    def __init__(self, bot : BenderBot.BenderBot):
        self.client = google.cloud.logging.Client()
        self.client.get_default_handler()
        self.client.setup_logging()
        self.bot = bot

    def __get_store_id(self, date: str, execution_id: str):
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        filter_str = (
            f'timestamp >= {date} AND '
            f'timestamp < {next_day.date()} AND '
            f'labels."execution_id": {execution_id}'
        )
        for entry in self.client.list_entries(filter_=filter_str):
            if entry.payload.startswith("{'date':"):
                response = entry.payload.replace('{', '').replace('}', '').replace('\'', '')
                return response

    def list_not_found_entries(self, date: str):
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        entries_list = []
        filter_str = (
            f'timestamp >= {date} AND '
            f'timestamp < {next_day.date()} AND '
            'text_payload: NotFound'
        )

        for entry in self.client.list_entries(filter_=filter_str):
            try:
                message = (
                    f'{entry.severity} 404 on task: {entry.labels["execution_id"]} \n'
                    f'Source: {entry.resource.labels["function_name"]} \n'
                    f'''Not Found: {entry.payload[
                                        entry.payload.index('404 GET'):
                                        entry.payload.index('?')
                                    ].split('%2F')[-1]} \n'''
                )

            except:
                message = (
                    f'{entry.severity} 404 on task: {entry.labels["execution_id"]} \n'
                    f'Source: {entry.resource.labels["function_name"]} \n'
                    f'Message: {entry.payload}'
                )

            finally:
                entries_list.append(message)

        return entries_list

    def list_dropped_lines(self, date: str):
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        entries_list = []
        filter_str = (
            f'timestamp >= {date} AND '
            f'timestamp < {next_day.date()} AND '
            'text_payload: has dropped'
        )

        for entry in self.client.list_entries(filter_=filter_str):
            try:
                lines = entry.payload[entry.payload.index("[{"):].replace('},', '},\n')
                message = (
                    f'Dropped lines on task: {entry.labels["execution_id"]} \n'
                    f'Source: {entry.resource.labels["function_name"]} \n'
                    f'{self.__get_store_id(date, entry.labels["execution_id"])} \n'
                    f'Class/Function: {entry.payload[:entry.payload.index(" has dropped")]} \n'
                    f'Lines: \n {lines} \n'
                )

                entries_list.append(message)

            except:
                message = f'Linha fora do padrão: \n{entry.payload} \n'

            finally:
                entries_list.append(message)

        return entries_list

    def list_query_errors(self, date: str):
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        entries_list = []
        filter_str = (
            f'timestamp >= {date} AND '
            f'timestamp < {next_day.date()} AND '
            'severity = ERROR AND '
            'text_payload: federated data'
        )
        entries = self.client.list_entries(filter_=filter_str)
        for entry in entries:
            try:
                reason = entry.payload[
                         entry.payload.index(".exceptions"):
                         entry.payload.index("\n", entry.payload.index(".exceptions"))
                ]
                message = (
                    f'Query ERROR on task: {entry.labels["execution_id"]} \n'
                    f'Source: {entry.resource.labels["function_name"]} \n'
                    f'{self.__get_store_id(date, entry.labels["execution_id"])} \n'
                    f'Reason: {reason} \n'
                )

            except:
                message = (
                    f'Unknown error on task {entry.labels["execution_id"]}'
                    f'Source: {entry.resource.labels["function_name"]} \n'
                    f'{self.__get_store_id(date, entry.labels["execution_id"])} \n'
                    f'Payload: {entry.payload} \n'
                )

            finally:
                entries_list.append(message)

        return entries_list


    def list_unknown_errors(self, date: str):
        next_day = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)
        entries_list = []
        filter_str = (
            f'timestamp >= {date} AND '
            f'timestamp < {next_day.date()} AND '
            'resource.type = cloud_function AND '
            'severity > WARNING'
        )
        entries = self.client.list_entries(filter_=filter_str)
        for entry in entries:
            contains = (
                    str(entry.payload).__contains__('federated data') or
                    str(entry.payload).__contains__('Request failed')
            )
            if not contains:
                message = (
                        f'Unknown {entry.severity} on task: {entry.labels["execution_id"]} \n'
                        f'{self.__get_store_id(date, entry.labels["execution_id"])} \n'
                        f'Source: {entry.resource.labels["function_name"]} \n'
                        f'Payload: {entry.payload} \n'
                    )

                entries_list.append(message)

        return entries_list


if __name__ == '__main__':
    output_bot = BenderBot.BenderBot()
    cloud_loggin = CloudLogging(output_bot)
    # not_found_entries = cloud_loggin.list_not_found_entries('2021-03-15')
    # print(f'Qtd de erros 404: {len(not_found_entries)}')
    # for entry in not_found_entries:
    #     print(entry)

    # dropped_lines = cloud_loggin.list_dropped_lines('2021-03-11')
    # print(f'Qtd de funções que droparam linhas: {len(dropped_lines)}')
    # for entry in dropped_lines:
    #     print(entry)

    # query_errors = cloud_loggin.list_query_errors('2021-02-14')
    # print(f'Qtd de funções com erro de query: {len(query_errors)}')
    # for entry in query_errors:
    #     print(entry)

    # unknown_errors = cloud_loggin.list_unknown_errors('2021-03-15')
    # print(f'Qtd de erros ainda não mapeados: {len(unknown_errors)}')
    # for entry in unknown_errors:
    #     print(entry)
