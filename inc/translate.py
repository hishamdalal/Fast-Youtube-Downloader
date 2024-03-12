from youtube_transcript_api.formatters import SRTFormatter


class mySRTFormatter(SRTFormatter):
    def _format_transcript_helper(self, i, time_text, line):
        # rtl_char = '‫'
        # rtl_char = '\u202B'
        # ascii_unsupported = '\u202B'
        
        # https://www.w3.org/International/questions/qa-bidi-unicode-controls

        start = u'\u200F' + u'\u202E' + u'\u202B'
        end = u'\u202C'
        
        text = ""
        ary = line['text'].split("\n")
        for l in ary:
            text += start + l + end + "\n"
        # rtl_char = str(ascii_unsupported.encode('utf-8'))
        # rtl_char = str(int('202B', 16).to_bytes(4, 'big'), 'utf_32_be')
        return "{}\n{}\n{}".format(i + 1, time_text, text)

