"""
샘플 로그 데이터 초기화 스크립트
"""
import json
import os
from .sample_log_generator import generate_all_sample_logs
from .agent_log_service import save_agent_log, ensure_logs_directory

def update_sample_products_with_log_ids():
    """샘플 제품 데이터에 agent_log_id 추가"""
    
    # 샘플 제품 데이터 로드
    products_file = 'data/sample_products.json'
    
    try:
        with open(products_file, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {products_file}")
        return False
    
    # 샘플 로그 생성
    sample_logs = generate_all_sample_logs()
    
    # 로그 ID를 리뷰 ID로 매핑
    log_id_map = {log.review_id: log.id for log in sample_logs}
    
    # 제품 데이터 업데이트
    updated = False
    for product in products_data.get('products', []):
        for review in product.get('reviews', []):
            review_id = review['id']
            
            # seller_response가 있는 리뷰에만 agent_log_id 추가
            if 'seller_response' in review and review_id in log_id_map:
                review['agent_log_id'] = log_id_map[review_id]
                updated = True
                print(f"리뷰 {review_id}에 로그 ID {log_id_map[review_id]} 추가")
    
    # 업데이트된 데이터 저장
    if updated:
        try:
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(products_data, f, ensure_ascii=False, indent=2)
            print(f"샘플 제품 데이터 업데이트 완료: {products_file}")
        except Exception as e:
            print(f"파일 저장 실패: {e}")
            return False
    
    # 로그 파일들 저장
    ensure_logs_directory()
    saved_count = 0
    
    for log in sample_logs:
        if save_agent_log(log):
            saved_count += 1
        else:
            print(f"로그 저장 실패: {log.id}")
    
    print(f"샘플 로그 파일 {saved_count}개 생성 완료")
    
    return True

def verify_sample_data():
    """샘플 데이터 검증"""
    
    # 제품 데이터 검증
    try:
        with open('data/sample_products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        total_reviews = 0
        reviews_with_logs = 0
        
        for product in products_data.get('products', []):
            for review in product.get('reviews', []):
                total_reviews += 1
                if 'agent_log_id' in review:
                    reviews_with_logs += 1
        
        print(f"총 리뷰 수: {total_reviews}")
        print(f"로그 ID가 있는 리뷰 수: {reviews_with_logs}")
        
    except Exception as e:
        print(f"제품 데이터 검증 실패: {e}")
        return False
    
    # 로그 파일 검증
    logs_dir = 'data/agent_logs'
    if os.path.exists(logs_dir):
        log_files = [f for f in os.listdir(logs_dir) if f.endswith('.json')]
        print(f"생성된 로그 파일 수: {len(log_files)}")
        
        # 몇 개 파일 내용 검증
        for i, filename in enumerate(log_files[:3]):
            try:
                with open(os.path.join(logs_dir, filename), 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                print(f"로그 파일 {filename}: OK (단계 수: {len(log_data.get('steps', []))})")
            except Exception as e:
                print(f"로그 파일 {filename}: 오류 - {e}")
    else:
        print("로그 디렉토리가 존재하지 않습니다.")
        return False
    
    return True

def clean_sample_logs():
    """기존 샘플 로그 정리"""
    logs_dir = 'data/agent_logs'
    
    if not os.path.exists(logs_dir):
        return
    
    deleted_count = 0
    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(logs_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    log_data = json.load(f)
                
                # 샘플 로그인지 확인
                if log_data.get('is_sample', False):
                    os.remove(file_path)
                    deleted_count += 1
            except Exception as e:
                print(f"파일 처리 중 오류: {filename} - {e}")
    
    print(f"기존 샘플 로그 {deleted_count}개 삭제")

if __name__ == "__main__":
    print("=== 샘플 로그 데이터 초기화 ===")
    
    # 기존 샘플 로그 정리
    clean_sample_logs()
    
    # 새로운 샘플 로그 생성 및 데이터 업데이트
    if update_sample_products_with_log_ids():
        print("샘플 데이터 업데이트 성공")
        
        # 검증
        if verify_sample_data():
            print("샘플 데이터 검증 완료")
        else:
            print("샘플 데이터 검증 실패")
    else:
        print("샘플 데이터 업데이트 실패")