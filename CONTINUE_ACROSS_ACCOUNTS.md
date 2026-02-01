# 🔄 How to Continue Work Across Different Claude Accounts

## 📋 The Problem
Claude has usage limits per account, so you need to switch between accounts to continue working.

---

## ✅ Solution: Context Handoff Document

Create a **PROJECT_CONTEXT.md** file that you upload to the new Claude account.

### 📄 Template: PROJECT_CONTEXT.md

```markdown
# Real Estate MIS - V2 Development Context

## 🎯 Current Status
**Date:** [Current Date]
**Phase:** Team Module Integration Complete
**Branch:** feature/commission-restructure
**Progress:** 50% of V2 restructure done

## ✅ What's Been Completed

### Phase 1: Database Models ✅
- Created TeamMember model (employees, revenue partners, owner)
- Created BusinessPartner model (builders, other brokerages)
- Redesigned CommissionStructure for proper flow tracking
- Updated Deal model with new fields
- Files: `core/models.py`

### Phase 2: Migration ✅
- Created migration script: `migrate_to_v2_comprehensive.py`
- Migrates Partner data to Team/Business Partners
- Recreates commission_structures table with V2 schema
- Adds new columns to deals table
- **Status:** Migration completed successfully

### Phase 3: Team Module ✅
- Backend: Repository + Service complete
- UI: TeamListPage + TeamMemberDialog complete
- Integration: Added to main window navigation
- **Status:** Fully functional, accessible from menu

## 📁 File Structure
```
MIS/
├── core/
│   └── models.py (UPDATED with V2 models)
├── modules/
│   └── team/ (NEW - COMPLETE)
│       ├── repositories/
│       │   └── team_repository.py
│       ├── services/
│       │   └── team_service.py
│       └── ui/
│           ├── team_list_page.py
│           ├── team_dialog.py
│           └── __init__.py
├── ui/
│   └── main_window.py (UPDATED - Team integrated)
├── migrate_to_v2_comprehensive.py (NEW)
└── [other existing files]
```

## 🔧 Recent Issues Fixed
1. TeamMemberRepository query error - FIXED
2. BaseRepository.create() argument error - FIXED
3. Main window integration - DONE

## 🎯 What Needs to Be Done Next

### Option 1: Business Partners Module (Recommended Next)
Similar to Team module:
- Create BusinessPartnerRepository
- Create BusinessPartnerService  
- Create BusinessPartnerListPage UI
- Create BusinessPartnerDialog UI
- Integrate into main window

### Option 2: Commission Redesign (Complex, save for later)
- Update CommissionRepository for V2 schema
- Update CommissionService with new flow logic
- Create Commission Wizard UI
- Implement builder → company → client → team flow

### Option 3: Update Existing Modules
- Update Deal Dialog with new fields
- Update Dashboard with Team metrics

## 💡 Key Architecture Decisions

### Commission Flow (V2 Logic)
**Builder Deal:**
```
Builder pays 5% → Company receives
  ↓
Split:
├─ 4% cashback to client
└─ 1% retained by company
       ├─ If Employee: 10% to employee, 90% to company
       ├─ If Revenue Partner: 60/40 split (configured)
       └─ If Owner: 100% to company
```

**Client Deal:**
```
Client pays 2% → Company receives
  ↓
├─ If Employee: 10% to employee, 90% to company
├─ If Revenue Partner: 60/40 split
└─ If Owner: 100% to company
```

### Team vs Business Partners
- **Team:** Internal people (employees, revenue partners, owner)
- **Business Partners:** External entities (builders, other brokerages)

## 🐛 Known Issues
- None currently

## 📝 Important Notes
- Old Partners module still exists (for backward compatibility)
- Database has both old and new tables
- Migration backs up old commission data to `commission_structures_backup`

## 🔗 Git Information
- **Current Branch:** feature/commission-restructure
- **Remote:** origin
- **Not merged to v2 yet** - waiting for completion

## 📞 How to Continue

When starting a new Claude session:
1. Upload this PROJECT_CONTEXT.md file
2. Say: "I'm continuing work on Real Estate MIS V2. Please read the context."
3. Specify what you want to work on next
4. Claude will understand where we left off!
```

---

## 🎯 How to Use This

### Step 1: Create the File
1. Copy the template above
2. Save as `PROJECT_CONTEXT.md` in your MIS folder
3. Update the "Current Status" section with latest info

### Step 2: When Switching Accounts
1. Open new Claude account (when limit hits)
2. Upload `PROJECT_CONTEXT.md`
3. Say: "I'm continuing the Real Estate MIS V2 project. Please read the context file."

### Step 3: Update After Each Session
After completing work:
1. Update "What's Been Completed" section
2. Update "Recent Issues Fixed"
3. Update "What Needs to Be Done Next"
4. Save for next session

---

## 📋 Quick Context Messages

### For New Sessions (After Uploading Context)
```
"I'm continuing work on Real Estate MIS V2 restructure. 
I've uploaded PROJECT_CONTEXT.md with our current progress.

Current status:
- Team module is complete and integrated
- Next: [What you want to work on]

Please review the context and let's continue!"
```

### For Specific Tasks
```
"I'm continuing Real Estate MIS V2 (context uploaded).
Team module is done. Now I want to build the Business Partners module.
It should be similar to Team module structure."
```

### For Bug Fixes
```
"Continuing Real Estate MIS V2 (context uploaded).
I'm getting this error: [paste error]
Can you help fix it?"
```

---

## 💾 What to Keep Track Of

### Always Include in Context:
1. ✅ What's completed (with file names)
2. ✅ What's in progress
3. ✅ What's next
4. ✅ Any known issues
5. ✅ Important architectural decisions
6. ✅ Recent changes/fixes

### Don't Need to Include:
- ❌ Entire file contents (too long)
- ❌ Detailed code (unless relevant to current issue)
- ❌ Old conversation history

---

## 🎨 Alternative: Use Git Commits

Instead of context file, you can also:
1. Commit all work to git
2. Push to GitHub
3. In new Claude session, say:
   ```
   "I'm working on Real Estate MIS V2.
   Check my latest commits on feature/commission-restructure branch
   to see what's been done.
   
   Latest commit: [commit message]
   Next: I want to build Business Partners module"
   ```

---

## 📊 Progress Tracking Template

Add this to your context file:

```markdown
## Progress Tracker
- [x] Database Models
- [x] Migration Script
- [x] Team Module Backend
- [x] Team Module UI
- [x] Team Integration
- [ ] Business Partners Backend
- [ ] Business Partners UI
- [ ] Business Partners Integration
- [ ] Commission Redesign
- [ ] Deal Module Updates
- [ ] Dashboard Updates
- [ ] Testing & Bug Fixes
```

---

## ✅ Summary

**To continue across accounts:**
1. Create `PROJECT_CONTEXT.md` with current status
2. Update it after each session
3. Upload to new Claude account
4. Say what you want to work on
5. Claude understands context and continues!

**This way:**
- ✅ No repetition of what's done
- ✅ Claude knows exactly where you are
- ✅ Can jump right into next task
- ✅ Preserves architectural decisions
- ✅ Tracks progress over time

---

**Create this file now and keep it updated!** 🚀
