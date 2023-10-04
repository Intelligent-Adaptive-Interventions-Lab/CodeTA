from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import logging
import docker
import json
import os

logger = logging.getLogger(__name__)

@csrf_exempt
def get_code_executor(request):
    if request.method == "GET":
        name = "code-executor"
        tag = request.GET.get('language', '')
        rebuild = request.GET.get('rebuild', False)

        if (tag == ''):
            return JsonResponse({"error": "Invalid request method"}, status=400)
        
        try:
            client = docker.from_env()

            if rebuild:
                build_context_path = os.path.join(settings.BASE_DIR, f'execute_env/{tag}')

                # Build the image and specify the tag
                image, _ = client.images.build(
                    path=build_context_path, 
                    tag=f"{name}:{tag}"
                )
            else:
                image = client.images.get(f"{name}:{tag}")
              
            return JsonResponse({
                'name': name,
                'tag': image.tags,
                'id': image.id
            }, status=200)
        except docker.errors.ImageNotFound:
            logger.critical(f"image {name}:{tag} not found")

            build_context_path = os.path.join(settings.BASE_DIR, f'execute_env/{tag}')

            # Build the image and specify the tag
            image, _ = client.images.build(
                path=build_context_path, 
                tag=f"{name}:{tag}"
            )

            # Return some information about the built image
            return JsonResponse({
                'name': name,
                'image_id': image.id,
                'image_tags': image.tags
            }, status=200)
        except docker.errors.APIError as e:
            # Handle general Docker API errors
            return JsonResponse({
                'error': f'Docker API error: {str(e)}',
            }, status=500)
        except Exception as e:
            # Handle unexpected errors
            return JsonResponse({
                'error': f'An unexpected error occurred: {str(e)}',
            }, status=500)

@csrf_exempt
def execute_code(request):
    if request.method == "POST":
        payload = json.loads(request.body.decode('utf-8'))
        language = payload.get('language')
        code = payload.get('code')
        test_cases = payload.get('testCases')

        results = []

        try:
            client = docker.from_env()
            _ = client.images.get(f"code-executor:{language}")

            for test_case in test_cases:
                logger.critical(f"code: {code}")

                try:
                    result = client.containers.run(
                        f"code-executor:{language}",
                        remove=True,  # Automatically remove the container when it exits
                        environment={"SCRIPT_TO_RUN": code}
                    )

                    logger.critical(f"result: {result}")
                    if result.decode("utf-8").strip() == test_case['expectedOutput'].strip():
                        results.append({"input": test_case['input'], "expected_output": test_case['expectedOutput'], "output": result.decode("utf-8").strip(), "status": "Pass"})
                    else:
                        results.append({"input": test_case['input'], "expected_output": test_case['expectedOutput'], "output": result.decode("utf-8").strip(), "status": "Fail"})
                except Exception as e:
                    results.append({"input": test_case['input'], "expected_output": test_case['expectedOutput'], "output": str(e), "status": "Error"})
        except Exception as e:
            return JsonResponse({"error": f"Error processing request: {str(e)}"}, status=500)

        return JsonResponse({"results": results})

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)
