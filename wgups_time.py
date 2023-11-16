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

        Time Complexity: Technically O(n), because of the string.split method, but the length of the 2 parameter that is
        being split will never be longer than 8, no matter how large the input of the program. Worse case: O(n), Avg
         Case: O(8) = O(1)

        Parameters:
            time(str): The time to be checked in standard time format (HH:MM:SS) as a string.

        Returns:
            bool: True if input parameter is a string, otherwise nothing gets returned. If not True, a TypeError is
            raised.
        """
        # If time format is (HH:MM:SS)
        if isinstance(time, str):
            input_check = time.split(':')

            if len(input_check) == 3:
                # Hour
                if not input_check[0].isnumeric():
                    raise ValueError(f'Hours must be numbers only.'
                                     f' {input_check[0]} is not a valid hour value.')
                if 0 <= int(input_check[0]) <= 23:
                    # Minute
                    if not input_check[1].isnumeric():
                        raise ValueError(f'Minutes must be numbers only.'
                                         f' {input_check[1]} is not a valid minute value.')
                    if 0 <= int(input_check[1]) <= 59:
                        # Second
                        if not input_check[2].isnumeric():
                            raise ValueError(f'Seconds must be numbers only.'
                                             f' {input_check[2]} is not a valid second value.')
                        if 0 <= int(input_check[2]) <= 59:
                            return True
                        else:
                            raise ValueError(f'Seconds must be between 0 and 59(inclusive).'
                                             f' {input_check[2]} is not a valid second value.')
                    else:
                        raise ValueError(f'Minutes must be between 0 and 59(inclusive).'
                                         f' {input_check[1]} is not a valid minute value.')
                else:
                    raise ValueError(f'Hours must be between 0 and 23(inclusive).'
                                     f' {input_check[0]} is not a valid hour value.')

            # If time format is (HH:MM)
            elif len(input_check) == 2:
                # Hour
                if not input_check[0].isnumeric():
                    raise ValueError(f'Hours must be numbers only.'
                                     f' {input_check[0]} is not a valid hour value.')
                if 0 <= int(input_check[0]) <= 23:

                    # Minute
                    if not input_check[1].isnumeric():
                        raise ValueError(f'Minutes must be numbers only.'
                                         f' {input_check[1]} is not a valid minute value.')
                    if 0 <= int(input_check[1]) <= 59:
                        return True
                    else:
                        raise ValueError(f'Minutes must be between 0 and 59(inclusive).'
                                         f' {input_check[1]} is not a valid minute value.')
                else:
                    raise ValueError(f'Hours must be between 0 and 23(inclusive).'
                                     f' {input_check[0]} is not a valid hour value.')
            else:
                raise ValueError(f'{input_check} is an invalid entry. Please check your entry and try again.')

        else:
            raise TypeError(f'{time} is an Invalid time entry.')

    def convert_string_time_to_int_seconds(self, time):
        """
        This method takes a string and returns the converted time in seconds as an int.

        Time Complexity: Technically O(n), because of the string.split and string.count methods, but the length of the
        parameter that is being split and counted will never be longer than 8, no matter how large the input of the
        program. Worse case: O(n), Avg Case: O(8) = O(1)

        Parameters:
            time(str): The time to be converted in standard time (HH:MM:SS) format.

        Returns:
            int: The formatted time (HH:MM:SS) as a string converted time in integer seconds.
        """
        if self.check_input(time):
            if time.count(':') == 1:
                time += ':00'
            (time_hr, time_min, time_sec) = time.split(':')  # [O(8)]

            return (int(time_hr) * 3600) + (int(time_min) * 60) + int(time_sec)

    @staticmethod
    def convert_int_seconds_to_string_time(seconds):
        """
        This method takes a time in seconds and returns the time in string format(HH:MM:SS).

        Time Complexity: O(1)

        Parameters:
            seconds(int): The time to be converted in seconds.

        Returns:
            str: The converted time in standard time format (HH:MM:SS) as a string.
        """
        if seconds >= 3600:

            hour = seconds // 3600

            minutes = (seconds % 3600) // 60
            if minutes < 10:
                minutes = '0' + str(minutes)
            else:
                minutes = str(minutes)

            seconds = seconds % 60
            if seconds < 10:
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
            if seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            return f'00:{minutes}:{seconds}'

    def add_time(self, time1, time2):
        """
        This method takes two times in string format and returns the sum of the two times in integer seconds.

        Time Complexity: O(1).

        Parameters:
            time1(str): The first time parameter in standard time (HH:MM:SS) format.
            time2(str): The second time parameter in standard time (HH:MM:SS) format.

        Returns:
            int: Sum of the two parameters in seconds.
        """
        if self.check_input(time1) and self.check_input(time2):
            return self.convert_string_time_to_int_seconds(time1) + self.convert_string_time_to_int_seconds(time2)

    def time_difference(self, time1, time2):
        """
        This method takes two times in string format and returns the difference in integer seconds. If the first
        variable, time1, is larger than the second variable, time2, then the method returns a positive number(difference
        in seconds), else it will return a negative number (difference in seconds). If there is no difference, 0 will be
        returned.

        Time Complexity: Technically O(n), because of the string.split and string.count methods, but the length of the 2
        parameters that are being split and counted will never be longer than 8, no matter how large the input of the
        program. Worse case: O(n), Avg Case: O(8) = O(1)

        Parameters:
            time1(str): The first time parameter in standard time (HH:MM:SS) format.
            time2(str): The second time parameter in standard time (HH:MM:SS) format.

        Returns:
            int: The difference between the two parameters in seconds.
        """

        if self.check_input(time1) and self.check_input(time2):  # [O(1)]

            if time1.count(':') == 1:
                time1 += ':00'
            (time1_hr, time1_min, time1_sec) = time1.split(':')

            if time2.count(':') == 1:
                time2 += ':00'
            (time2_hr, time2_min, time2_sec) = time2.split(':')

            total_seconds_1 = int(time1_hr) * 3600 + int(time1_min) * 60 + int(time1_sec)
            total_seconds_2 = int(time2_hr) * 3600 + int(time2_min) * 60 + int(time2_sec)

            return total_seconds_1 - total_seconds_2
