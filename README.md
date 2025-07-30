# 깃모지 설명
| 아이콘   | 코드        | 설명                                  | 원문                             |
|----------|-------------|---------------------------------------|----------------------------------|
| 🎨       | `:art:`     | 코드의 구조/형태 개선                   | Improve structure / format of the code. |
| ⚡️       | `:zap:`     | 성능 개선                              | Improve performance.              |
| 🔥       | `:fire:`    | 코드/파일 삭제                         | Remove code or files.            |
| 🐛       | `:bug:`     | 버그 수정                              | Fix a bug.                        |
| 🚑       | `:ambulance:` | 긴급 수정                          | Critical hotfix.                  |
| ✨       | `:sparkles:` | 새 기능                                | Introduce new features.           |
| 💄       | `:lipstick:` | UI/스타일 파일 추가/수정               | Add or update the UI and style files. |
| 🎉       | `:tada:`    | 프로젝트 시작                          | Begin a project.                  |
|🚀        | `:rocket:`    | CI/CD                         | Deploying stuff                 |
| ✅       | `:white_check_mark:` | 테스트 추가/수정                  | Add or update tests.              |
| 💚       | `:green_heart:` | CI 빌드 수정                         | Fix CI Build.                     |
| ♻️       | `:recycle:` | 코드 리팩토링                           | Refactor code.                    |
| 🔨       | `:hammer:`  | 개발 스크립트 추가/수정                | Add or update development scripts. |
| 🔀       | `:twisted_rightwards_arrows:` | 브랜치 합병                   | Merge branches.                  |
| 📝       | `:memo:` | 문서 수정                   | Update Docs.                 |


## 🪴 Branch Convention (GitHub Flow)

- `main`: 배포 가능한 브랜치, 항상 배포 가능한 상태를 유지
- `develop`: 기능 개발 후 배포 전 최종 테스트를 위한 브랜치
- `feature/{description}`: 새로운 기능을 개발하는 브랜치
    - 예: `feature/social-login`

### Flow

1. `main` 브랜치에서 새로운 브랜치를 생성.
2. 작업을 완료하고 커밋 메시지에 맞게 커밋.
3. Pull Request를 생성 / 팀원들의 리뷰.
4. 리뷰가 완료되면 `main` 브랜치로 병합.
5. 병합 후, 필요시 배포.

**예시**:

```bash
# 새로운 기능 개발
git checkout -b feature/social-login

# 작업 완료 후, main 브랜치로 병합
git checkout main
git pull origin main
git merge feature/social-login
git push origin main
```
