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

        if seconds >= 3600:
            hour = seconds // 3600
            minutes = (seconds % 3600) // 60
            print(f'minutes id: {minutes}')
            if minutes < 10:
                minutes = '0' + str(minutes)
            else:
                minutes = str(minutes)
            seconds = seconds % 60
            if seconds % 10 == 0:
                seconds = str(seconds) + '0'
            elif seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            return f'{hour}:{minutes}:{seconds}'
        else:
            minutes = seconds // 60
            if minutes < 10:
                minutes = '0' + str(minutes)
            else:
                minutes = str(minutes)
            seconds = int(seconds % 60)
            if seconds % 10 == 0:
                seconds = str(seconds) + '0'
            elif seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            return f'{minutes}:{seconds}'

    def add_time(self, time1, time2):

        if self.check_input(time1) and self.check_input(time2):
            total_seconds = self.convert_time_to_seconds(time1) + self.convert_time_to_seconds(time2)
            return self.convert_seconds_to_time(total_seconds)

    def time_difference(self, time1, time2):
        """
        This method takes two times in string format and returns the difference. If the first variable, time1, is larger
        than the second variable, time2, then the method returns a positive number(difference in seconds), else it will
        return a negative number (difference in seconds). If there is no difference, 0 will be returned.

        Parameters:
            time1(str): First time parameter.
            time2(str): Second time parameter.

        Return:
            int: Difference between the two parameters in seconds.
        """

        if self.check_input(time1) and self.check_input(time2):
            (time1_hr, time1_min, time1_sec) = time1.split(':')
            (time2_hr, time2_min, time2_sec) = time2.split(':')

            total_seconds_1 = int(time1_hr) * 3600 + int(time1_min) * 60 + int(time1_sec)
            total_seconds_2 = int(time2_hr) * 3600 + int(time2_min) * 60 + int(time2_sec)

            diff = total_seconds_1 - total_seconds_2

            return diff
