from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Art, Bid
from .serializers import RegisterSerializer, ArtSerializer, BidSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])  
        user.save()
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Registration successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_art(request):
    user = request.user
    data = request.data
    image = request.FILES.get('image')

    art = Art.objects.create(
        user=user,
        name=data.get('name'),
        image=image,
        description=data.get('description'),
        start_price=data.get('start_price'),
        fixed_price=data.get('fixed_price')
    )

    serializer = ArtSerializer(art, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_arts(request):
    arts = Art.objects.all().order_by('-created_at')
    serializer = ArtSerializer(arts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def art_detail(request, art_uuid):
    art = get_object_or_404(Art, uuid=art_uuid)
    serializer = ArtSerializer(art, many=False)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_bid(request, art_uuid):
    art = get_object_or_404(Art, uuid=art_uuid)
    user = request.user
    bid_amount = request.data.get('bid_amount')

    if bid_amount is None or float(bid_amount) <= art.start_price:
        return Response({'error': 'Bid must be higher than the start price'}, status=status.HTTP_400_BAD_REQUEST)

    new_bid = Bid.objects.create(art=art, user=user, amount=bid_amount)

    art.start_price = float(bid_amount)
    art.save()

    return Response({'message': 'Bid placed successfully', 'new_price': art.start_price}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_bids(request, art_uuid):
    art = get_object_or_404(Art, uuid=art_uuid)
    bids = art.bids.all().order_by('-timestamp')
    serializer = BidSerializer(bids, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
