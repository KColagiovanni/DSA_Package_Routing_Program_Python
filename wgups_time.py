class WgupsTime:

    @staticmethod
    def check_input(time):
        if not isinstance(time, str):
            raise TypeError(f'{time} must be a string.')
        # elif not <hr:min:sec present>
        #     raise ValueError('Time format (HH:MM:SS) is incorrect.')
        else:
            return True

    def convert_time_to_seconds(self, time):
        if self.check_input(time):
            (time_hr, time_min, time_sec) = time.split(':')
            return int(time_hr * 3600) + int(time_min * 60) + int(time_sec)

    @staticmethod
    def convert_seconds_to_time(seconds):

        if seconds > 3600:
            total_hours = seconds // 3600
            total_minutes = (seconds % 3600) // 60
            # total_second =

            print(f'Hours: {total_hours}')
            print(f'Minutes: {total_minutes}')
            # print(f'Seconds: {total_seconds}')

            # return f'{total_hours}:{total_minutes}:{total_seconds}'

    def add_time(self, time1, time2):

            if self.check_input(time1) and self.check_input(time2):
                total_seconds = self.convert_time_to_seconds(time1) + self.convert_time_to_seconds(time2)
                return self.convert_seconds_to_time(total_seconds)

    def time_difference(self, time1, time2):

        if self.check_input:
            (time1_hr, time1_min, time1_sec) = time1.split(':')
            (time2_hr, time2_min, time2_sec) = time2.split(':')

            total_seconds_1 = int(time1_hr * 3600) + int(time1_min * 60) + int(time1_sec)
            total_seconds_2 = int(time2_hr * 3600) + int(time2_min * 60) + int(time2_sec)