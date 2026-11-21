# research_package v1 (editor-agnostic contract)
Produced by media_researcher; consumed by any editor adapter (YouTube today; a TikTok adapter later). The core never assumes aspect ratio, length or platform.

**asset_manifest.json** → `{project, topic, assets[]}`; each asset: asset_id, filename (relative, only if a file was collected), asset_type (image|screenshot|video|article), original_url, page_url, source_name, source_author, publication_date, narration_segment[] (plan segment ids), suggested_timestamp[] ({start,end,caption_excerpt}), relevance_score (0-1 keyword coverage, NOT a truth check), relevance_reason, resolution, duration, license_information, usage_permissions, download_status, verification_status, editor_eligible (bool), eligibility_reason, review_thumbnail, used_in_final_video.
**research_assets.json** (from stage.py) → `{usable[], blocked[]}`: usable = file exists + opens + passes the editor's stager + eligible (open licence or human-approved). blocked always lists the reason.
**permissions.json** → `{approvals:[{url, asset_id, approved_by, approved_on, note}], commit_approved_media:false}`: written only on a human's instruction.
**Adapter responsibilities (not core):** crop/aspect (16:9, 9:16 safe zones), duration/pacing, caption placement, credit rendering. The core only guarantees sourced files + attribution + permission state.
