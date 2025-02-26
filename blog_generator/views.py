from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import send_email_token
from .models import Profile,BlogPost
import uuid   # USED FOR EMAIL TOKEN GENERATION
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json,os
import assemblyai as aai
import google.generativeai as genai
import yt_dlp    # USED FOR INTERACTING WITH YOUTUBE
from textwrap import dedent
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

@login_required
def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data': request.POST}
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pswrd = request.POST.get('pswrd')
        rpswrd = request.POST.get('rpswrd')

        # Validation checks for password, username, etc.

        fields = {
            "fname": "Please enter your First name",
            "lname": "Please enter your Last name",
            "uname": "Please enter your Username",
            "email": "Please enter a valid email"
        }

        for field, error_msg in fields.items():
            if not locals()[field]:  # Dynamically check variable value
                messages.error(request, error_msg)
                context["has_error"] = True

        if len(pswrd) < 6:
            messages.add_message(request, messages.ERROR, "Password should be at least 6 characters")
            context['has_error'] = True

        if pswrd != rpswrd:
            messages.add_message(request, messages.ERROR, "Password mismatch")
            context['has_error'] = True

        if User.objects.filter(username=uname).exists():
            messages.add_message(request, messages.ERROR, "Username already exists")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'signup.html', context)
        
        else:
            # Create the user
            user_obj = User.objects.create_user(
                first_name=fname,
                last_name=lname,
                username=uname,
                email=email,
                password=pswrd,
            )
            user_obj.save()

            p_obj = Profile.objects.create(
                user = user_obj,
                email_token = str(uuid.uuid4())
            )

            send_email_token(email,p_obj.email_token, p_obj.user.first_name)

            messages.add_message(request, messages.SUCCESS, "Email verification needed, check your email")
            return redirect('blog_generator:user_login')

    return render(request, 'signup.html')


def verify(request, token):
    try:
        obj = Profile.objects.get(email_token=token)
        obj.is_verified = True
        obj.save()
        messages.success(request, "Your account has been verified.")
        return redirect('blog_generator:user_login')
    except Profile.DoesNotExist:
        messages.error(request, "Invalid Token")
        return redirect('blog_generator:user_login')


def user_login(request):
    if request.method == 'POST':
        context = {'has_error': False}
        uname = request.POST.get('uname')
        pswrd = request.POST.get('pswrd')

        if not uname:
            messages.error(request, "Please enter your Username")
            context['has_error'] = True
        if not pswrd:
            messages.error(request, "Please enter your Password")
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'login.html', context)

        user = authenticate(username=uname, password=pswrd)

        if user:
            profile = Profile.objects.filter(user=user).first()
            if profile and not profile.is_verified:
                messages.error(request, "Your email is not verified. Please check your email.")
                return render(request, 'login.html', context)  # Prevent login and reload page

            login(request, user)
            messages.success(request, f"Login Success, Welcome {user.first_name}")
            return redirect('blog_generator:index')

        else:
            messages.error(request, "Invalid Username or Password")
    
    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('blog_generator:user_login')


@login_required
def all_blogs(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all-blogs.html', {"blog_articles": blog_articles})

@login_required
def blog_details(request,i):
    p = BlogPost.objects.get(id=i)
    return render(request, 'blog-details.html',{"product":p})


# Placeholder for blog generation (add actual logic as needed)
@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data.get('link')

            if not yt_link:
                return JsonResponse({'error': 'No YouTube link provided'}, status=400)

            # Debugging: Log received YouTube link
            print(f"Received YouTube link: {yt_link}")

            # Simulated functions (ensure these work correctly)
            title = yt_title(yt_link)
            transcription = get_transcription(yt_link)
            if "error" in transcription:
                return JsonResponse({'error': transcription["error"]}, status=500)
            if not transcription:
                messages.error(request, "Failed to get transcript")
                return JsonResponse({'error': 'Failed to get transcript'}, status=500)

            # Generate blog content using OpenAI
            blog_content = generate_blog_from_transcription(transcription)

            if not blog_content:
                messages.error(request, "Failed to generate blog article")
                return JsonResponse({'error': 'Failed to generate blog article'}, status=500)
            
            # save blog
            new_blog_article = BlogPost.objects.create(
                user = request.user,
                youtube_title = title,
                youtube_link = yt_link,
                generated_content = blog_content,
            )
            new_blog_article.save()

            return JsonResponse({'content': blog_content})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"Server Error: {str(e)}")  # Debugging logs
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# --- Step 1: Extract Video Title ---
def yt_title(link):
    """Fetch the title of a YouTube video using yt-dlp."""
    try:
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            title = info.get("title", "Unknown Title")
            print(f"Fetched Title: {title}")  # Debugging output
            return title
    except yt_dlp.utils.DownloadError as e:
        return f"Download Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# --- Step 2: Download YouTube Audio ---
def download_audio(link):
    """Download audio from a YouTube video using yt-dlp."""
    try:
        # Ensure MEDIA_ROOT exists
        output_path = settings.MEDIA_ROOT
        os.makedirs(output_path, exist_ok=True)

        # Output file path
        output_file = os.path.join(output_path, "%(title)s.%(ext)s")

        # yt-dlp options
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": output_file,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        print(f"Audio downloaded successfully: {filename}")
        return {"file_path": filename}
    except Exception as e:
        return {"error": f"Error downloading audio: {str(e)}"}

# --- Step 3: Get Audio Transcription ---
def get_transcription(link):
    """Transcribe audio from a YouTube video using AssemblyAI."""
    result = download_audio(link)

    # Check if there's an error
    if "error" in result:
        return {"error": result["error"]}

    file_path = result["file_path"]

    # Load API Key securely
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    if not aai.settings.api_key:
        return {"error": "AssemblyAI API Key is missing. Check .env file."}

    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path)

        return {"transcript": transcript.text}

    except Exception as e:
        return {"error": f"Transcription failed: {str(e)}"}

# --- Step 4: Get Blog from Transcription ---
def generate_blog_from_transcription(transcription):
    """Generate a blog post from a transcription using Gemini API."""
    
    api_key = os.getenv("GEMINI_API_KEY")  
    print(os.getenv("GEMINI_API_KEY"))


    if not api_key:
        return "Error: Gemini API Key is missing. Check .env file."

    # Configure the Gemini API
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")

    # Clean indentation for proper formatting
    prompt = dedent(f"""\
    Rewrite the following YouTube video transcript into a well-structured blog article.

    **Formatting Rules:**
    - The **main heading** should be on its own line, followed by a blank line before the introduction.
    - Use **bold subheadings** for different sections.
    - Ensure each paragraph is clearly separated with a blank line.
    - Keep the article **concise, engaging, and under 500 words**.

    Here is the transcript:
    {transcription}
    """)

    try:
        response = model.generate_content(prompt)
        
        # Debugging: print the full response
        # print("Gemini API Response:", response)

        # Extract the response text safely
        return getattr(response, "text", "Error: No valid response from Gemini API.").strip()

    except Exception as e:  
        print(f"Gemini API Error: {e}")
        return "Error generating blog. Please try again later."


def custom_404(request):
    return render(request, "404.html", status=404)