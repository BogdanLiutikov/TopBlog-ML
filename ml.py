import math
import easyocr
import numpy
from cv2 import imread
import re

# load ocr
reader = easyocr.Reader(['en', 'ru'])


def use_ocr(image_path):
    result = reader.readtext(image_path, low_text=0.1, text_threshold=0.5)
    return result


def get_box_center(box):
    x = (box[0][0] + box[1][0]) / 2
    y = (box[3][1] + box[3][1]) / 2
    return [x, y]


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


re_digit = re.compile(r'\d+[., ]?\d+\s?(?:млн|тыс|к|м)?', re.IGNORECASE)
re_vk_target = re.compile(r'подписчик|участник|друзей', re.IGNORECASE)
re_vk_subscribers = re.compile(r'подписчик', re.IGNORECASE)


def vk_subscribers(recognitions):
    matches = []
    digit_matches = []
    for recognition in recognitions:
        if re_vk_target.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_digit.search(recognition[1]) is not None:
            digit_matches.append(recognition)
    key_digit = []
    for match in matches:
        if re_digit.search(match[1]) is not None:
            key_digit.append(re_digit.search(match[1])[0])
        else:
            match_center = get_box_center(match[0])
            digit_matches.sort(key=lambda digit: dist(get_box_center(digit[0]), match_center))
            key_digit.append(re_digit.search(digit_matches[0][1])[0])
    return key_digit


def get_matches_and_digits(recognitions):
    matches = []
    digit_matches = []
    for recognition in recognitions:
        if re_vk_target.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_digit.search(recognition[1]) is not None:
            digit_matches.append(recognition)
    return matches, digit_matches


re_yt_subscribers = re.compile(r'подписчик', re.IGNORECASE)
re_yt_views = re.compile(r'просмотр', re.IGNORECASE)


def yt_subscribers(recognitions):
    matches = []
    digit_matches = []
    for recognition in recognitions:
        if re_yt_subscribers.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_digit.search(recognition[1]) is not None:
            digit_matches.append(recognition)
    key_digit = []
    for match in matches:
        if re_digit.search(match[1]) is not None:
            key_digit.append(re_digit.search(match[1])[0])
        else:
            match_center = get_box_center(match[0])
            digit_matches.sort(key=lambda digit: dist(get_box_center(digit[0]), match_center))
            key_digit.append(re_digit.search(digit_matches[0][1])[0])
    return key_digit


def yt_views(recognitions):
    matches = []
    digit_matches = []
    for recognition in recognitions:
        if re_yt_views.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_digit.search(recognition[1]) is not None:
            digit_matches.append(recognition)
    key_digit = []
    for match in matches:
        if re_digit.search(match[1]) is not None:
            key_digit.append(re_digit.search(match[1])[0])
        else:
            match_center = get_box_center(match[0])
            size = math.dist(match_center, match[0][0])
            digit_matches_radius = list(filter(
                lambda digit_match: dist(get_box_center(digit_match[0]), match_center) <= size,
                digit_matches))
            if len(digit_matches_radius) > 0:
                key_digit.append(re_digit.search(digit_matches_radius[0][1])[0])
            else:
                digit_matches.sort(key=lambda digit: (abs(get_box_center(digit[0])[1] - match_center[1])))
                key_digit.append(re_digit.search(digit_matches[0][1])[0])
    return key_digit


re_zn_reads = re.compile(r'дочитывания', re.IGNORECASE)


def zn_reads(recognitions):
    matches = []
    digit_matches = []
    for recognition in recognitions:
        if re_zn_reads.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_digit.search(recognition[1]) is not None:
            digit_matches.append(recognition)
    key_digit = []
    for match in matches:
        match_center = get_box_center(match[0])
        size = math.dist(match_center, match[0][0])
        digit_matches_radius = list(filter(
            lambda digit_match: dist(get_box_center(digit_match[0]), match_center) <= size,
            digit_matches))
        if len(digit_matches_radius) > 0:
            digit_matches.sort(key=lambda digit: math.dist(get_box_center(digit[0]), match_center))
            key_digit.append(re_digit.search(digit_matches[0][1])[0])
        else:
            digit_matches = list(
                filter(lambda digit_match: get_box_center(digit_match[0])[1] > match_center[1], digit_matches))
            digit_matches.sort(key=lambda digit: (abs(get_box_center(digit[0])[0] - match_center[0])))
            key_digit.append(re_digit.search(digit_matches[0][1])[0])
    if len(key_digit) == 2:
        return [key_digit[1]]
    else:
        return key_digit


re_tg_vr = re.compile(r'\bvr\b|\berr\b', re.IGNORECASE)
re_tg_vr_percent = re.compile(r'\d+\s?%', re.IGNORECASE)


def tg_vr(recognitions):
    matches = []
    percent_matches = []
    for recognition in recognitions:
        if re_tg_vr.search(recognition[1]) is not None:
            matches.append(recognition)
        elif re_tg_vr_percent.search(recognition[1]) is not None:
            percent_matches.append(recognition)
    key_digit = []
    for match in matches:
        if re_tg_vr_percent.search(match[1]) is not None:
            key_digit.append(re_digit.search(match[1])[0])
        else:
            match_center = get_box_center(match[0])
            size = math.dist(match_center, match[0][0]) * 3
            percent_matches_radius = list(filter(
                lambda percent_match: dist(get_box_center(percent_match[0]), match_center) <= size,
                percent_matches))
            if len(percent_matches_radius) <= 0:
                percent_matches.sort(key=lambda digit: math.dist(get_box_center(digit[0]), match_center))
                key_digit.append(re_digit.search(percent_matches[0][1])[0])
            else:
                percent_matches = list(
                    filter(lambda percent_match: get_box_center(percent_match[0])[1] < match_center[1],
                           percent_matches))
                percent_matches.sort(key=lambda digit: (abs(get_box_center(digit[0])[0] - match_center[0])))
                key_digit.append(re_digit.search(percent_matches[0][1])[0])
    return key_digit


def analyze_results(all_recognitions, platform):
    result = []
    if platform.lower() == 'vk':
        result = vk_subscribers(all_recognitions)
    elif platform.lower() == 'yt':
        result = yt_subscribers(all_recognitions), yt_views(all_recognitions)
    elif platform.lower() == 'tg':
        result = tg_vr(all_recognitions)
    elif platform.lower() == 'zn':
        result = zn_reads(all_recognitions)
    if len(result) > 0:
        return result[0]
    else:
        return 0


def model_predict(img, platform):
    image = numpy.array(img)
    results = use_ocr(image)
    analyze = analyze_results(results, platform)
    return analyze


if __name__ == '__main__':
    image_path = 'data/tg/images/1b1d9d87-2625-4f82-ba56-2d8a9d5172cf.png'
    image = imread(image_path)
    results = use_ocr(image)
    print(results)
    print(analyze_results(results, 'tg'))
