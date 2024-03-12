from pytube.exceptions import RegexMatchError
from pytube import YouTube, Playlist
import pytube.request
from pytube.cli import on_progress
from pytube.exceptions import PytubeError

from youtube_transcript_api import YouTubeTranscriptApi

from icecream import ic

import re
import sys
import os
import threading
import datetime

import inc.helper as helper
import inc.paths as paths
import inc.log as log
from inc.config import YPD_Config

from inc.translate import mySRTFormatter


pytube.request.default_range_size = 100000




class fastYTD:
    
    match = {}
    downloads_dir = '.'
    _type = 'Video'
    quality = 'Mid'
    ext = 'mp4'
    skip_existing = True
    download_translate = False
    translate_from = 'en'
    translate_to = 'ar'
    config = None
    options = {}
    success = []
    fail = []
    
    # ------------------------------------------------------- 
    def __init__(self):
        try:
            self.config = YPD_Config()            
        except Exception as e:
            log.msg(e)
            
        self.options['MAIN'] = {}
        self.options['TRANSLATE'] = {}
        
        print("\t\t==================================")
        print("\t\tWELCOME TO FAST YOUTUBE DOWNLOADER")
        print("\t\t==================================\n")
        
        while(True):
            self.config.read()
            self.init_config()
            
            self.url = input("Select One:\n- Enter Youtube or Playlist `URL` to start downloading\n- Enter `h` for help\n\t -> ")
            
            # GET DOWNLOAD INFO =====================
            if len(self.url) > 5 :
                
                url_type = self.check_url(self.url)
            
                download_type = ""
            
                if url_type['playlist'] and url_type['video']:
                    which_to_download = input("Download Playlist or just one file?\n\t1) Playlist\n\t2) One file\n\t-> ")
                
                    if which_to_download == '1':
                        download_type = 'playlist'
                    
                    elif which_to_download == '2':
                        download_type = 'one_file'
                        
                elif url_type['playlist']:
                    download_type = 'playlist'
                    
                elif url_type['video']:
                    download_type = 'one_file'

                else:
                    print("Invalid URL")
                    continue
                
                self.set_type_options()
                self.set_quality_options()
                self.set_translate_options()
                
                # START DOWNLOADING ===============================
                if download_type == 'playlist':
                    log.line('\nDownload type', 'Playlist')
                    self.fetch_playlist(self.url)
                    
                elif download_type == 'one_file':
                    log.line('\nDownload type', 'One file')
                    self.fetch_one_file(self.url)
            
            elif self.url == 'h':
                self.show_help()
                    
            else:
                # CHANGE SETTINGS ===========================
                self.set_config_path()
                self.set_config_skip_exists()
                self.set_config_type()
                self.set_config_resolution()
                self.set_config_download_translation()
                if self.download_translate == 'True':
                    self.set_config_translate_from()
                    self.set_config_translate_to()
                
                ic(self.options)
                print("")
                
            _continue = input("Continue?\n\t1) Yes\n\t2) No exit\n\t-> ")
            if _continue == '1':
                continue
            else:
                break
        
        sys.exit(0) 
    # ------------------------------------------------------- 
    def set_type_options(self):
        if self.config.get('MAIN', 'type') != 'Ask':
            _type = self.config.get('MAIN', 'type')
        else:
            _type = input("Select Type:\n\t1) Video\n\t2) Audio\n\t-> ")
        
        if _type=='2' or _type =='Audio':
            self._type  = 'Audio'
            self.ext    = 'mp3'
        else:
            self._type = 'Video'
            self.ext    = 'mp4'
    # ------------------------------------------------------- 
    def set_quality_options(self):
        if self.config.get('MAIN', 'resolution') != 'Ask':
            quality = self.config.get('MAIN', 'resolution')
        else:
            quality = input("Quality:\n\t1) High\n\t2) Mid\n\t3) Low\n\t-> ")
            
        if quality == '1' or quality == 'Hight':
            self.quality = 'High'
        elif quality == '2' or quality == 'Mid':
            self.quality = 'Mid'
        elif quality == '3' or quality == 'Low':
            self.quality = 'Low'
        else:
            self.quality = 'Mid'
    # ------------------------------------------------------- 
    def set_translate_options(self):
        if self.config.get('TRANSLATE', 'download') != 'Ask':
            translate = self.config.get('TRANSLATE', 'download')
        else:
            translate = input("Translate?:\n\t1) Yes\n\t2) No\n\t-> ")
        if translate == '1' or translate == 'True':
            self.download_translate = True
            
            if self.config.get('TRANSLATE', 'from') != 'Ask':
                self.translate_from = self.config.get('TRANSLATE', 'from')
            else:
                self.translate_from  = input('translate from: en \n\t-> ')
            
            if self.config.get('TRANSLATE', 'to') != 'Ask':
                self.translate_to = self.config.get('TRANSLATE', 'to')
            else:
                self.translate_to    = input('translate to: ar \n\t-> ')
        
    # ------------------------------------------------------- 
    def init_config(self):
        try:
            self.downloads_dir = self.config.get(section='MAIN', key='downloads_dir')
            self._type = self.config.get(section='MAIN', key='type')
            self.skip_existing = self.config.get(section='MAIN', key='skip_existing')
            self.resolution = self.config.get(section='MAIN', key='resolution')
            self.download_translate = self.config.get(section='TRANSLATE', key='download')
            self.translate_from = self.config.get(section='TRANSLATE', key='from')
            self.translate_to = self.config.get(section='TRANSLATE', key='to')
        except Exception as e:
            log.msg(e)
    # ------------------------------------------------------- 
    def set_config_path(self):
        config_path = input("Download path:\n\t1) Downloads directory\n\t2) Current directory\n\t3) Custom directory\n\t4) Ask me every time\n\t-> ")
        
        match config_path:
            case '1':
                downloads_dir = paths.get_downloads_path()
            case '2':
                downloads_dir = '.'
            case '4':
                downloads_dir = 'Ask'    
            case '3':
                custom_path = input("- Entre a valid path for downloads:\n\t-> ")
                if custom_path and paths.is_valid_path(custom_path, True):
                    downloads_dir = config_path
                    
                else:
                    downloads_dir = paths.get_downloads_path()
                    print("Invalid path, default path = " + downloads_dir)
        
        self.downloads_dir = downloads_dir
        self.options['MAIN']['downloads_dir'] = downloads_dir
        self.config.save('MAIN', 'downloads_dir', downloads_dir)
    # ------------------------------------------------------- 
    def set_config_skip_exists(self):
        config_skip_exists = input("Skip exists files:\n\t1) Yes\n\t2) No\n\t3) Ask me every time\n\t-> ")
        
        match config_skip_exists:
            case '1':
                skip_existing = 'True'
            case '2':
                skip_existing = 'False'
            case '3':
                skip_existing = 'Ask'
                
        self.skip_existing = skip_existing
        self.options['MAIN']['skip_existing'] = skip_existing
        self.config.save('MAIN', 'skip_existing', skip_existing)
    # ------------------------------------------------------- 
    def set_config_type(self):    
        config_type = input("Download type:\n\t1) Video\n\t2) Audio\n\t3) Ask me every time\n\t-> ")
        
        match config_type:
            case '1':
                _type = 'Video'
            case '2':
                _type = 'Audio'
            case '3':
                _type = 'Ask'
        
        self._type = _type
        self.options['type'] = _type
        self.config.save('MAIN', 'type', _type)
    # ------------------------------------------------------- 
    def set_config_resolution(self):
        config_resolution = input("Download resolution:\n\t1) High\n\t2) Mid\n\t3) low\n\t4) Ask me every time\n\t-> ")

        match config_resolution:
            case '1':
                resolution = 'High'
            case '2':
                resolution = 'Mid'
            case '3':
                resolution = 'Low'
            case '4':
                resolution = 'Ask'
        
        self.resolution = resolution
        self.options['resolution'] = resolution
        self.config.save('MAIN', 'resolution', resolution)
    # ------------------------------------------------------- 
    def set_config_download_translation(self):
        config_translate = input("Download translation:\n\t1) Yes\n\t2) No\n\t3) Ask me every time\n\t-> ")
        
        match config_translate:
            case '1':
                download_translate = 'True'
            case '2':
                download_translate = 'False'
            case '3':
                download_translate = 'Ask'
        
        self.download_translate = download_translate
        self.options['TRANSLATE']['download'] = download_translate
        self.config.save('TRANSLATE', 'download', download_translate)
    # ------------------------------------------------------- 
    def set_config_translate_from(self):
        config_translate_from = input(f"translate from:\n\t1) en\n\t2) other:\n\t3) Ask me every time\n\t-> ")
        match config_translate_from:
            case '1':
                translate_from = 'en'
            case '2':
                translate_from = input('Enter language key for example `en`:\n\t')
            case '3':
                translate_from = 'Ask'
        
        self.translate_from = translate_from
        self.options['TRANSLATE']['from'] = translate_from
        self.config.save('TRANSLATE', 'from', translate_from)
    # ------------------------------------------------------- 
    def set_config_translate_to(self):
        config_translate_to = input(f"translate to:\n\t1) ar\n\t2) other\n\t3) Ask me every time\n\t")
        match config_translate_to:
            case '1':
                translate_to = 'ar'
            case '2':
                translate_to = input('Enter language key for example `ar`:\n\t')
            case '3':
                translate_to = 'Ask'
        
        self.translate_to = translate_to
        self.options['TRANSLATE']['to'] = translate_to
        self.config.save('TRANSLATE', 'to', translate_to)
    # ------------------------------------------------------- 
    def show_help(self):
        log.text_separator('Help')
        log.line('Download', 'Enter youtube video or playlist `url` and press `enter` to start download.')
        log.line('Help', 'Enter `h` and press `enter` to show help')
        log.line('Setting', 'Press `Enter` to change settings like `resolution` and `translation`')
        log.line('Exit', 'Press `ctrl+c` to exit')
        log.line('About', 'https://github.com/hishamdalal')
        print("")
    # ------------------------------------------------------- 
    def check_url(self, url: str):
        if url == "":
            return False
        
        regex_video_playlist     = (r'(https?:\/\/)?(www.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)\/((?:embed\/|v\/|watch\?v=)(\S+)).?(\&list=(\S+)).?')
        regex_playlist  = (r'(https?:\/\/)?(www.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)\/playlist\?list=(\S+)/?')
        regex_video     = (r'(https?:\/\/)?(www.)?(youtube\.com|youtu\.be|youtube-nocookie\.com)\/((?:embed\/|v\/|watch\?v=)(\S+))')

        match = {'video': False, 'playlist': False}

        try:
            playlist_match = re.match(string=url, pattern=regex_playlist)
            video_match = re.match(string=url, pattern=regex_video)
            video_playlist_match = re.match(string=url, pattern=regex_video_playlist)
            
            if playlist_match:
                match['playlist'] = True
                
                
            elif video_playlist_match:
                groups = video_playlist_match.groups()
                if len(groups) > 6 and groups[5].startswith('&list='):
                    match['playlist'] = True
                    match['video'] = True
                    # print(video_match.group(6))
                    
                elif len(groups)>3 and groups[3].startswith('watch?v='):
                    match['video'] = True
                    # print(video_match.group(4))
                            
            elif video_match:
                match['video'] = True
        except Exception as e:
            helper.show_error(e)
        finally: 
            return match
    # ----------------------------------------------------------------------------    
    def fetch(self, url: str):
        yt = None
        try:
            yt = YouTube(url)
            
            log.text_separator('Start')
            
            # threading.Thread(target=yt.register_on_progress_callback(self.tqdm_progress_callback)).start()
            threading.Thread(target=yt.register_on_progress_callback(on_progress)).start()
            # yt.register_on_complete_callback(self.complete_progress)
            
            try:
                yt.check_availability()
            except Exception as e:
                helper.show_error(e)
            
        except Exception as e:
            helper.show_error(e)
        except RegexMatchError as e:
            helper.show_error(e)
            log.line("RegexMatchError", "URL is not correct, {e}\n")
        except helper.AgeRestrictionError as e:
            helper.show_error(e)
            log.line("AgeRestrictionError", e)
        except helper.UnavailableError as e:
            helper.show_error(e)
            log.line("UnavailableError", e)
        except helper.PytubeError as e:
            helper.show_error(e)
            log.line("PyTubeError", e)
        except Exception as e:
            # log.line("Unknown Error", e)
            log.line("Error", e)        
            helper.show_error(e)
        
        finally:
            return yt
    # ----------------------------------------------------------------------------    
    def fetch_one_file(self, url: str, downloads_dir=None, file_number=0):
        if downloads_dir == None:
            downloads_dir = self.downloads_dir
        
        yt = self.fetch(url)
        streams = None
        res = []
        resource = None
        
        
        filename = str(helper.slugify(yt.title))
        if file_number > 0:
            filename = str(file_number) + ') ' + filename
            
        filename_with_ext = filename + '.' + self.ext

        self.show_info(yt)

        
        if yt:
            if self._type == 'Audio':
                streams = yt.streams.filter(only_audio=True, progressive=False)
            else:
                streams = yt.streams.filter(only_audio=False, progressive=True)
            
            
            if len(streams) > 0:
                for stream in streams:
                    res.append(stream.resolution)
                
                # self.pbar = tqdm(total=stream.filesize, unit="bytes")
                file_size = str(stream.filesize_mb) + " mb"
                log.line('Size', file_size)
                
                match self.quality:
                    case 'High':
                        resource = streams.get_highest_resolution()
                        log.line('Quality', res[-1])
                    case 'Low':
                        resource = streams.get_lowest_resolution()
                        log.line('Quality', res[0])
                    case 'Mid':
                        mid_res = helper.list_middle(res)
                        
                        log.line('Quality', mid_res)
                        
                        if self._type == 'Audio':
                            resource = streams.get_by_itag(itag=int(mid_res))
                        else:
                            resource = streams.get_by_resolution(resolution=mid_res)
                
                if resource:
                    try:
                        
                        # https://stackoverflow.com/a/6904509/2269902
                        # threading.Thread(target=test, args=(arg1,), kwargs={'arg2':arg2}).start()

                        # threading.Thread(target=self.do_download, args=(resource, downloads_dir,filename_with_ext)).start()

                        resource.download(output_path=downloads_dir, filename=filename_with_ext, skip_existing=self.skip_existing)
                        
                        if self.download_translate == True:
                            self.do_download_translate(downloads_dir, filename_with_ext, yt.video_id)
                        
                        self.success.append(filename)                        
                            
                    except Exception as e:
                        helper.show_error(e)
                        self.fail.append(filename)
                else:
                    log.line('Error', 'No resource found!')        
    # ----------------------------------------------------------------------------    
    def do_download(self, resource, downloads_dir, filename_with_ext):
        resource.download(output_path=downloads_dir, filename=filename_with_ext, skip_existing=self.skip_existing)
        if self.download_translate == True:
            self.do_download_translate(downloads_dir, filename_with_ext, yt.video_id)
        
    # ----------------------------------------------------------------------------    
    def fetch_playlist(self, url: str):
        playlist = Playlist(url)
        
        if len(playlist):
            
            log.line('Playlist', playlist.title)
            log.separator()
            
            downloads_dir = self.downloads_dir + '/' + helper.slugify(playlist.title)
            
            i = 0
            for yt in playlist:
                i += 1
                try:
                    log.line('No', i)
                    self.fetch_one_file(url=yt, downloads_dir=downloads_dir, file_number=i)
                    print("\n")
                    # log.separator()
                    
                except Exception as e:
                    print(e)
                    continue
            
            self.success_report()
            self.fail_report()
            
    # ----------------------------------------------------------------------------    
    def download_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress = (bytes_downloaded / total_size) * 100
        str_progress = f"progress: {progress:.2f}%"
        
        print(str_progress)
    # ----------------------------------------------------------------------------    
    def complete_progress(self, stream, file_path):
        print("Done ")
    # ----------------------------------------------------------------------------
    def tqdm_progress_callback(self, stream, data_chunk, bytes_remaining) -> None:
        
        self.pbar.update(len(data_chunk))


    # ----------------------------------------------------------------------------
    def do_download_translate(self, downloads_dir, filename, video_id):
        try:
            download_path = downloads_dir +"/"+filename+".srt"
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript([self.translate_from, 'en'])
            
            if transcript.is_translatable:
                selected_lang = transcript.translate(self.translate_to).fetch(preserve_formatting=True)

                # https://youtu.be/tvtb6Bg8CFU
                # more info: https://www.w3.org/International/questions/qa-bidi-unicode-controls

                if self.translate_to == 'ar':
                    formater = mySRTFormatter()
                else:
                    formater = SRTFormatter()
                    
                srt_formatted = formater.format_transcript(selected_lang)
                with open(download_path, 'w', encoding='utf-8') as srt_file:
                    srt_file.write(srt_formatted)
                    
                log.line('translate', 'downloaded successfully\n')
        
        except Exception as e:
            helper.show_error(e)    
    # ----------------------------------------------------------------------------
    def show_info(self, yt):
        log.line('title', yt.title)
        log.line('author', yt.author)
        log.line('publish_date', yt.publish_date)
        log.line('length', str(datetime.timedelta(seconds=yt.length)))
        # log.line('rating', yt.rating)
        log.line('views', yt.views)
        log.line('keywords', yt.keywords)
        log.line('video_id', yt.video_id)
        log.line('watch_url', yt.watch_url)
        # helper.dump(yt)
    # ----------------------------------------------------------------------------
    def success_report(self):
        if len(self.success):
            log.text_separator("Success")
            for line in self.success:
                log.msg(line)    
            log.separator()
    # ----------------------------------------------------------------------------
    def fail_report(self):
        if len(self.fail):
            log.text_separator("Fail")
            for line in self.fail:
                log.msg(line)
            log.separator()
    # ----------------------------------------------------------------------------


fastYTD()