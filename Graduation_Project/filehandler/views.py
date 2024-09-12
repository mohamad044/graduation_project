from django.shortcuts import render, redirect
from .pinata_post import upload_to_pinata
from .blockchain import store_hash_in_blockchain
from .forms import UploadFileForm
from .deploy_contract import deploy_contract  

def deploy_contract_view(request):
    if request.method == 'POST':
        contract_address = deploy_contract()
        return render(request, 'deploy.html', {'contract_address': contract_address})
    
    return render(request, 'deploy.html')
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file
            uploaded_file = form.cleaned_data['file']
            file_path = f'media/{uploaded_file.name}'

            # Save file to the media directory
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Upload the file to Pinata (IPFS)
            ipfs_hash = upload_to_pinata(file_path)
            if ipfs_hash:
                # Store the hash in the blockchain
                transaction = store_hash_in_blockchain(ipfs_hash)
                if transaction:
                    return render(request, 'upload.html', {'form': form, 'message': 'File uploaded and hash stored successfully'})
                else:
                    return render(request, 'upload.html', {'form': form, 'error': 'Failed to store hash in blockchain'})
            else:
                return render(request, 'upload.html', {'form': form, 'error': 'Failed to upload file to IPFS'})
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

