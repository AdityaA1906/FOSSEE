from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import FileResponse, HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.pdfgen import canvas
from .models import EquipmentData, UploadHistory, DatasetHistory
from .serializers import EquipmentDataSerializer, UploadHistorySerializer, UserSerializer, DatasetHistorySerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Create new user with username and password"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=request.data.get('first_name', ''),
        last_name=request.data.get('last_name', '')
    )
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
        'message': 'User created successfully'
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login with username and password"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """Mock Google Login endpoint - in production, verify Google token"""
    # For demo purposes, create/login a test user
    email = request.data.get('email', 'demo@example.com')
    username = email.split('@')[0]  # Use email prefix as username
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={'email': email, 'first_name': 'Demo', 'last_name': 'User'}
    )
    
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and parse CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    
    try:
        # Read CSV with pandas - handle different encodings
        try:
            content = csv_file.read().decode('utf-8')
        except UnicodeDecodeError:
            csv_file.seek(0)
            content = csv_file.read().decode('latin-1')
        
        df = pd.read_csv(io.StringIO(content))
        
        # Create DatasetHistory
        dataset_history = DatasetHistory.objects.create(
            user=request.user,
            filename=csv_file.name,
            original_csv=csv_file,
            row_count=len(df)
        )
        
        # Create upload history (legacy support)
        upload_history = UploadHistory.objects.create(
            user=request.user,
            filename=csv_file.name,
            row_count=len(df),
            dataset=dataset_history
        )
        
        # Calculate summary statistics for storage
        stats = {
            'total_count': len(df),
            'flowrate_avg': float(df['Flowrate'].mean()),
            'pressure_avg': float(df['Pressure'].mean()),
            'temperature_avg': float(df['Temperature'].mean()),
            'types': df['Type'].value_counts().to_dict() if 'Type' in df.columns else {}
        }
        dataset_history.summary_data = stats
        dataset_history.save()

        # Parse and save equipment data
        equipment_objects = []
        for _, row in df.iterrows():
            equipment_objects.append(EquipmentData(
                upload=upload_history,
                dataset=dataset_history,
                equipment_name=row.get('Equipment Name', row.get('equipment_name', '')),
                equipment_type=row.get('Type', row.get('equipment_type', '')),
                flowrate=float(row.get('Flowrate', row.get('flowrate', 0))),
                pressure=float(row.get('Pressure', row.get('pressure', 0))),
                temperature=float(row.get('Temperature', row.get('temperature', 0)))
            ))
        
        EquipmentData.objects.bulk_create(equipment_objects)
        
        return Response({
            'message': 'File uploaded successfully',
            'upload_id': upload_history.id,
            'dataset_id': dataset_history.id,
            'rows_processed': len(df),
            'summary': stats
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_equipment_data(request):
    """Get all equipment data with optional filtering"""
    upload_id = request.query_params.get('upload_id')
    dataset_id = request.query_params.get('dataset_id')
    
    queryset = EquipmentData.objects.all()
    if dataset_id:
        queryset = queryset.filter(dataset_id=dataset_id)
    elif upload_id:
        queryset = queryset.filter(upload_id=upload_id)
    
    serializer = EquipmentDataSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_statistics(request):
    """Calculate summary statistics"""
    upload_id = request.query_params.get('upload_id')
    dataset_id = request.query_params.get('dataset_id')
    
    queryset = EquipmentData.objects.all()
    if dataset_id:
        queryset = queryset.filter(dataset_id=dataset_id)
    elif upload_id:
        queryset = queryset.filter(upload_id=upload_id)
    
    if not queryset.exists():
        return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    
    # Convert to DataFrame for easy statistics
    data = list(queryset.values('flowrate', 'pressure', 'temperature', 'equipment_type'))
    df = pd.DataFrame(data)
    
    stats = {
        'total_count': len(df),
        'flowrate': {
            'mean': float(df['flowrate'].mean()),
            'min': float(df['flowrate'].min()),
            'max': float(df['flowrate'].max()),
            'std': float(df['flowrate'].std())
        },
        'pressure': {
            'mean': float(df['pressure'].mean()),
            'min': float(df['pressure'].min()),
            'max': float(df['pressure'].max()),
            'std': float(df['pressure'].std())
        },
        'temperature': {
            'mean': float(df['temperature'].mean()),
            'min': float(df['temperature'].min()),
            'max': float(df['temperature'].max()),
            'std': float(df['temperature'].std())
        },
        'equipment_types': df['equipment_type'].value_counts().to_dict()
    }
    
    return Response(stats)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_upload_history(request):
    """Get last 5 datasets"""
    history = DatasetHistory.objects.filter(user=request.user).order_by('-upload_date')[:5]
    serializer = DatasetHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_details(request, pk):
    """Get specific dataset details"""
    try:
        dataset = DatasetHistory.objects.get(pk=pk, user=request.user)
        serializer = DatasetHistorySerializer(dataset)
        return Response(serializer.data)
    except DatasetHistory.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request):
    """Generate PDF report with statistics and data"""
    upload_id = request.data.get('upload_id')
    dataset_id = request.data.get('dataset_id')
    
    # Get data
    if dataset_id:
        queryset = EquipmentData.objects.filter(dataset_id=dataset_id)
        dataset = DatasetHistory.objects.get(id=dataset_id)
        filename = dataset.filename
    elif upload_id:
        queryset = EquipmentData.objects.filter(upload_id=upload_id)
        upload = UploadHistory.objects.get(id=upload_id)
        filename = upload.filename
    else:
        queryset = EquipmentData.objects.all()
        filename = "All Data"
    
    if not queryset.exists():
        return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
    
    # Convert to DataFrame
    data = list(queryset.values('equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature'))
    df = pd.DataFrame(data)
    
    # Calculate statistics
    stats = {
        'total_count': len(df),
        'flowrate_mean': df['flowrate'].mean(),
        'pressure_mean': df['pressure'].mean(),
        'temperature_mean': df['temperature'].mean(),
    }
    
    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#00d4ff'),
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#b794f6'),
        spaceAfter=12,
    )
    
    # Title
    elements.append(Paragraph("Chemical Equipment Parameter Visualizer", title_style))
    elements.append(Paragraph("FOSSE Program - Data Analysis Report", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Report Info
    report_info = f"""
    <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>Dataset:</b> {filename}<br/>
    <b>Total Equipment Count:</b> {stats['total_count']}
    """
    elements.append(Paragraph(report_info, styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", heading_style))
    
    stats_data = [
        ['Parameter', 'Average', 'Min', 'Max', 'Std Dev'],
        ['Flowrate', f"{df['flowrate'].mean():.2f}", f"{df['flowrate'].min():.2f}", 
         f"{df['flowrate'].max():.2f}", f"{df['flowrate'].std():.2f}"],
        ['Pressure', f"{df['pressure'].mean():.2f}", f"{df['pressure'].min():.2f}", 
         f"{df['pressure'].max():.2f}", f"{df['pressure'].std():.2f}"],
        ['Temperature', f"{df['temperature'].mean():.2f}", f"{df['temperature'].min():.2f}", 
         f"{df['temperature'].max():.2f}", f"{df['temperature'].std():.2f}"],
    ]
    
    stats_table = Table(stats_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00d4ff')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0f0f0')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
    ]))
    
    elements.append(stats_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment Data Table (All rows)
    elements.append(Paragraph("Full Equipment Data Log", heading_style))
    
    data_rows = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temp']]
    for _, row in df.iterrows():
        data_rows.append([
            str(row['equipment_name'])[:30],
            str(row['equipment_type'])[:20],
            f"{row['flowrate']:.2f}",
            f"{row['pressure']:.2f}",
            f"{row['temperature']:.2f}"
        ])
    
    data_table = Table(data_rows, colWidths=[2.0*inch, 1.5*inch, 1*inch, 1*inch, 0.9*inch], repeatRows=1)
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#b794f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.beige])
    ]))
    
    elements.append(data_table)
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Return as file response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    return response
