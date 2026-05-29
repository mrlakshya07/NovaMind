from supabase_client import supabase

try:
    response = (
        supabase
        .table("study_sessions")
        .select("*")
        .execute()
    )

    print("✅ Supabase connected successfully")
    print(response.data)

except Exception as e:
    print("❌ Connection failed")
    print(e)