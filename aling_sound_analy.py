import numpy as np
from scipy.io.wavfile import read
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

###############################
# 함수 정의
###############################
def get_spectrum(filename):
    fs, data = read(filename)
    # float 변환
    sig = data.astype(np.float32)/32767.0
    N = len(sig)
    W = fft(sig)
    freqs = fftfreq(N, 1/fs)
    half = N//2
    return fs, freqs[:half], np.abs(W[:half]) / N

def find_peaks_in_spectrum(freqs, mag, height_threshold=0.001):
    # 피크 찾기
    peaks, _ = find_peaks(mag, height=height_threshold)
    return freqs[peaks], mag[peaks]

def fold_frequency(f_h, fs_target):
    # f_h 주파수를 fs_target으로 다운샘플링했을 때 폴딩되는 주파수 계산
    # N은 f_h를 가장 가까운 정수배 fs_target으로 매핑
    N = int(round(f_h / fs_target))
    return abs(f_h - N * fs_target)

def match_peaks(original_peaks, aliased_peaks):
    # 폴딩 후 주파수를 계산해 aliased_peaks 중 가장 가까운 피크를 매칭
    matched = []
    for f_h in original_peaks:
        # 폴딩 후 예상 주파수
        f_alias = fold_frequency(f_h, fs_target=4000)
        # aliased_peaks와 f_alias 사이 오차 최소인 것 고르기
        diff = np.abs(aliased_peaks - f_alias)
        idx = np.argmin(diff)
        matched.append((f_h, f_alias, aliased_peaks[idx], diff[idx]))
    return matched

###############################
# 메인 처리
###############################

# 원본과 다운샘플링 후 파일 이름 (가정)
original_file = "original_highfreq_sine.wav"
aliased_file = "aliased_doremi.wav"

# 스펙트럼 얻기
fs_orig, freqs_orig, mag_orig = get_spectrum(original_file)
fs_aliased, freqs_aliased, mag_aliased = get_spectrum(aliased_file)

# 피크 검출
orig_peaks_freq, orig_peaks_mag = find_peaks_in_spectrum(freqs_orig, mag_orig, height_threshold=0.001)
aliased_peaks_freq, aliased_peaks_mag = find_peaks_in_spectrum(freqs_aliased, mag_aliased, height_threshold=0.001)

# 원본 피크 중 나이퀴스트(2000 Hz) 이상인 것만 폴딩 관심
# (4000 Hz 다운샘플 시 Nyquist=2000 Hz)
high_peaks = orig_peaks_freq[orig_peaks_freq > 2000]

matches = match_peaks(high_peaks, aliased_peaks_freq)

###############################
# 결과 테이블 출력
###############################
print("Original Fs:", fs_orig, "Aliased Fs:", fs_aliased)
print("Matches (OriginalFreq, FoldedFreq(Expected), AliasedPeakFreq(Matched), Diff):")
for m in matches:
    print("Orig: {:.2f} Hz, Folded Expect: {:.2f} Hz, Matched: {:.2f} Hz, Diff: {:.2f} Hz".format(m[0], m[1], m[2], m[3]))

###############################
# 추가 설명
###############################
# matches 리스트에 담긴 각 행:
# (원본 고주파 피크, 예상 폴딩 주파수, 실제 다운샘플 후 매칭된 피크 주파수, 주파수 차이)
#
# 이를 통해 원본 스펙트럼상의 특정 고주파 성분이 다운샘플 후 스펙트럼의 어느 부분으로 폴딩되었는지 정량적으로 확인 가능.
