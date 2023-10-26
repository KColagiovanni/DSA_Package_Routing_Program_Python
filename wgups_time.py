class WgupsTime:
    """
    Convert string time in HH:MM:SS format to integer time in seconds and vice versa, and also add or subtract two
    different times.

    Attributes: None
    """

    @staticmethod
    def check_input(time):
        """
        This method checks time it was provided and verifies that it's type is string. It returns True if the input
         parameter is a string and raises a TypeError if it is not a string.

        Time Complexity: O(1)

        Parameter:
            time(str):

        Return:
            True if input parameter is a string, otherwise nothing gets returned, but a TypeError is raised.
        """

        if isinstance(time, str):
            input_check = time.split(':')
            print(len(input_check))
            print(input_check)
            if len(input_check) == 3:
                # print('Its good')
                # print(len(input_check))
                # print(input_check)
                return True
            elif len(input_check) == 2:
                time += ':00'
                return True
            else:
                return False
        else:
            raise TypeError(f'{time} must be a string.')

    def convert_string_time_to_int_seconds(self, time):
        """
        This method takes a string and returns the converted time in seconds as an int.

        Time Complexity: O(8) ==> O(1)

        Parameter:
            time(str):

        Return:
            The converted time as an int.
        """

        if self.check_input(time):
            (time_hr, time_min, time_sec) = time.split(':')  # [O(8)
            return int(time_hr * 3600) + int(time_min * 60) + int(time_sec)

    @staticmethod
    def convert_int_seconds_to_string_time(seconds):
        """
        This method takes a time in seconds and returns the time in string format(HH:MM:SS).

        Time Complexity: O(1)

        Parameter:
            seconds(int):

        Return:
            The converted time as a string in (HH:MM:SS) format.
        """

        if seconds >= 3600:
            hour = seconds // 3600
            minutes = (seconds % 3600) // 60
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
            return f'00:{minutes}:{seconds}'

    def add_time(self, time1, time2):
        """
        This method takes two times in string format and returns the sum of the two times.

        Time Complexity: The time complexity for this method is O(1).

        Parameter:
            time1(str): First time parameter.
            time2(str): Second time parameter.

        Return:
            int: Sum of the two Parameter in seconds.
        """

        if self.check_input(time1) and self.check_input(time2):
            total_seconds = (
                    self.convert_string_time_to_int_seconds(time1) + self.convert_string_time_to_int_seconds(time2)
            )
            return self.convert_int_seconds_to_string_time(total_seconds)

    def time_difference(self, time1, time2):
        """
        This method takes two times in string format and returns the difference. If the first variable, time1, is larger
        than the second variable, time2, then the method returns a positive number(difference in seconds), else it will
        return a negative number (difference in seconds). If there is no difference, 0 will be returned.

        Time Complexity: Technically O(n), because of the string.split method, but the length of the 2 Parameter that
        are being split will never be longer than 8, no matter how large the input of the program. Worse case: O(n),
        Avg Case: O(8) = O(1)

        Parameter:
            time1(str): First time parameter.
            time2(str): Second time parameter.

        Return:
            int: Difference between the two Parameter in seconds.
        """

        if self.check_input(time1) and self.check_input(time2):  # [O(1)

            (time1_hr, time1_min, time1_sec) = time1.split(':')
            (time2_hr, time2_min, time2_sec) = time2.split(':')

            total_seconds_1 = int(time1_hr) * 3600 + int(time1_min) * 60 + int(time1_sec)
            total_seconds_2 = int(time2_hr) * 3600 + int(time2_min) * 60 + int(time2_sec)

            diff = total_seconds_1 - total_seconds_2

            return diff
