#!/bin/bash
# PTCGP YouTube 影片下載腳本
# 用法: ./download_yt.sh "https://www.youtube.com/watch?v=..."

VIDEO_URL="$1"
OUTPUT_DIR="${2:-/home/node/.openclaw/workspace-celesteela/video3}"

if [ -z "$VIDEO_URL" ]; then
    echo "用法: $0 <YouTube URL> [輸出目錄]"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"
cd "$OUTPUT_DIR"

echo "下載影片: $VIDEO_URL"
/tmp/yt-dlp -f "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]" \
    -o "%(title)s.%(ext)s" \
    "$VIDEO_URL"

echo "下載完成: $OUTPUT_DIR"
