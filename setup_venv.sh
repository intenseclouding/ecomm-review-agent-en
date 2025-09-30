#!/bin/bash

# venv 삭제 (있으면)
if [ -d ".venv" ]; then
    rm -rf .venv
fi

# venv 생성
python3 -m venv .venv

# venv 활성화
source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# AWS 환경변수 설정
export AWS_DEFAULT_REGION=us-west-2
export AWS_REGION=us-west-2

echo "가상환경 설정 완료!"
echo "AWS Region이 us-west-2로 설정되었습니다."
