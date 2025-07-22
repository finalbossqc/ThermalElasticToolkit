import meshio as mio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
from scipy.interpolate import griddata, LinearNDInterpolator
from scipy.spatial import Delaunay
import os
import matplotlib.tri as mtri

class VTUAnimator:
    def __init__(self, data_dir="./data", dt=1e-12):
        self.data_dir = data_dir
        self.dt = dt
        self.meshes = []
        self.points = None
        self.data = None
        self.interpolation_grid = None
        self.grid_x = None
        self.grid_y = None
        self.grid_z = None
        
    def load_data(self):
        """Load PVTU files and extract mesh data from all pieces"""
        import xml.etree.ElementTree as ET
        
        # Get list of PVTU files
        pvtu_files = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.pvtu'):
                pvtu_files.append(file)
        
        # Sort frames numerically if they have numeric prefixes
        try:
            pvtu_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
        except:
            pvtu_files.sort()
        
        print(f"Found {len(pvtu_files)} PVTU frames")
        
        # Load meshes by parsing PVTU files and combining pieces
        for i, pvtu_file in enumerate(pvtu_files):
            pvtu_path = os.path.join(self.data_dir, pvtu_file)
            
            try:
                # Parse PVTU XML to get piece filenames
                tree = ET.parse(pvtu_path)
                root = tree.getroot()
                
                # Find all Piece elements
                pieces = root.findall('.//Piece')
                piece_files = [piece.get('Source') for piece in pieces]
                
                print(f"Loading frame {i+1}/{len(pvtu_files)}: {pvtu_file} ({len(piece_files)} pieces)")
                
                # Load and combine all pieces for this frame
                combined_points = []
                combined_data = {}
                
                for j, piece_file in enumerate(piece_files):
                    piece_path = os.path.join(self.data_dir, piece_file)
                    
                    try:
                        piece_mesh = mio.read(piece_path)
                        
                        # Accumulate points
                        combined_points.append(piece_mesh.points)
                        
                        # Accumulate point data
                        for key, values in piece_mesh.point_data.items():
                            if key not in combined_data:
                                combined_data[key] = []
                            combined_data[key].append(values)
                        
                    except Exception as e:
                        print(f"  Warning: Could not load piece {piece_file}: {e}")
                
                # Combine all pieces into single arrays
                if combined_points:
                    frame_points = np.vstack(combined_points)
                    frame_data = {}
                    for key, value_list in combined_data.items():
                        frame_data[key] = np.concatenate(value_list)
                    
                    # Create a mock mesh object to maintain compatibility
                    class MockMesh:
                        def __init__(self, points, point_data):
                            self.points = points
                            self.point_data = point_data
                    
                    mock_mesh = MockMesh(frame_points, frame_data)
                    self.meshes.append(mock_mesh)
                    
                    # Set points from first frame
                    if i == 0:
                        self.points = frame_points
                
            except Exception as e:
                print(f"Error loading {pvtu_file}: {e}")
        
        # Extract data arrays
        self.data = []
        for mesh in self.meshes:
            self.data.append(mesh.point_data)
        
        self.data = np.array(self.data, dtype=object)  # Use object dtype for variable-length arrays
        print(f"Loaded {len(self.meshes)} frames with combined mesh data")
        
    def setup_interpolation_grid(self, grid_resolution=100):
        """Setup regular grid for interpolation"""
        if self.points is None:
            self.load_data()
        
        # Define grid bounds with some padding
        x_min, x_max = self.points[:, 0].min(), self.points[:, 0].max()
        y_min, y_max = self.points[:, 1].min(), self.points[:, 1].max()
        z_min, z_max = self.points[:, 2].min(), self.points[:, 2].max()
        
        # Add 5% padding
        x_pad = 0.05 * (x_max - x_min)
        y_pad = 0.05 * (y_max - y_min)
        z_pad = 0.05 * (z_max - z_min)
        
        # Create regular grid
        x_grid = np.linspace(x_min - x_pad, x_max + x_pad, grid_resolution)
        y_grid = np.linspace(y_min - y_pad, y_max + y_pad, grid_resolution)
        z_grid = np.linspace(z_min - z_pad, z_max + z_pad, grid_resolution//2)
        
        self.grid_x, self.grid_y = np.meshgrid(x_grid, y_grid)
        self.grid_z = z_grid
        
        print(f"Interpolation grid setup: {grid_resolution}x{grid_resolution} points")
        
    def interpolate_data_2d(self, data_values, method='linear'):
        """Interpolate point data onto regular 2D grid using linear shape functions"""
        if self.grid_x is None:
            self.setup_interpolation_grid()
        
        # Extract 2D coordinates
        points_2d = self.points[:, :2]
        grid_points = np.column_stack([self.grid_x.ravel(), self.grid_y.ravel()])
        
        # Use scipy's griddata for linear interpolation (uses triangulation internally)
        interpolated = griddata(points_2d, data_values, grid_points, 
                              method=method, fill_value=0.0)
        
        return interpolated.reshape(self.grid_x.shape)
    
    def interpolate_data_3d(self, data_values, z_slice=None):
        """Interpolate point data in 3D space"""
        if self.grid_x is None:
            self.setup_interpolation_grid()
        
        if z_slice is None:
            z_slice = np.mean(self.points[:, 2])
        
        # Create 3D grid points at the specified z-slice
        grid_points_3d = np.column_stack([
            self.grid_x.ravel(), 
            self.grid_y.ravel(), 
            np.full(self.grid_x.size, z_slice)
        ])
        
        # Use LinearNDInterpolator for 3D interpolation
        interpolator = LinearNDInterpolator(self.points, data_values, fill_value=0.0)
        interpolated = interpolator(grid_points_3d)
        
        return interpolated.reshape(self.grid_x.shape)
    
    def create_smooth_magnitude_animation(self, save_path="smooth_velocity_magnitude.gif", 
                                    grid_resolution=150, z_slice=None):
        """Create smooth animation of velocity magnitude using interpolation on a 2D slice"""
        if self.data is None:
            self.load_data()
        
        # Determine the z-coordinate for the slice
        z_min, z_max = self.points[:, 2].min(), self.points[:, 2].max()
        
        if z_slice is None:
            actual_z_slice = np.median(self.points[:, 2])
            print(f"No z_slice specified, using median: {actual_z_slice:.6f}")
        else:
            # Find the closest z-coordinate in the mesh
            unique_z = np.unique(self.points[:, 2])
            closest_idx = np.argmin(np.abs(unique_z - z_slice))
            actual_z_slice = unique_z[closest_idx]
            print(f"Requested z_slice: {z_slice:.6f}, using closest available: {actual_z_slice:.6f}")
        
        print(f"Z-coordinate range: [{z_min:.6f}, {z_max:.6f}]")
        
        self.setup_interpolation_grid(grid_resolution)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Calculate velocity magnitude for all frames and interpolate
        print("Interpolating velocity magnitude data for 2D slice...")
        interpolated_magnitudes = []
        
        for i, frame_data in enumerate(self.data):
            u = frame_data['u']
            v = frame_data['v'] 
            w = frame_data['w']
            magnitude = np.sqrt(u**2 + v**2 + w**2)
            
            # Use 3D interpolation to get slice data at specified z-coordinate
            interp_magnitude = self.interpolate_data_3d(magnitude, z_slice=actual_z_slice)
            interpolated_magnitudes.append(interp_magnitude)
            
            print(f"  Processed frame {i+1}/{len(self.data)}")
        
        interpolated_magnitudes = np.array(interpolated_magnitudes)
        
        # Set up color scaling
        vmin = np.min(interpolated_magnitudes)
        vmax = np.max(interpolated_magnitudes)
        
        # Create smooth contour plot
        contour = ax.contourf(self.grid_x, self.grid_y, interpolated_magnitudes[0], 
                            levels=50, vmin=vmin, vmax=vmax)
        
        # Add contour lines for better definition
        contour_lines = ax.contour(self.grid_x, self.grid_y, interpolated_magnitudes[0], 
                                levels=20, alpha=0.3, linewidths=0.5)
        
        # Overlay mesh points that are close to the slice z-coordinate
        z_tolerance = 0.1 * (z_max - z_min)  # 10% of z-range as tolerance
        slice_mask = np.abs(self.points[:, 2] - actual_z_slice) <= z_tolerance
        slice_points = self.points[slice_mask]
        
        if len(slice_points) > 0:
            scatter = ax.scatter(slice_points[:, 0], slice_points[:, 1], 
                            c='white', s=10, alpha=0.7, linewidth=0.5)
        
        # Formatting
        ax.set_xlabel('X coordinate', fontsize=12)
        ax.set_ylabel('Y coordinate', fontsize=12)
        ax.set_title(f'Velocity Magnitude Evolution - Z-slice at {actual_z_slice:.6f}', fontsize=14)
        ax.set_aspect('equal')
        
        # Time text
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        def animate(frame):
            # Clear previous contours
            for coll in ax.collections:
                if len(slice_points) > 0 and coll != scatter:
                    coll.remove()
                elif len(slice_points) == 0:
                    coll.remove()
            
            # Create new contours
            contour = ax.contourf(self.grid_x, self.grid_y, interpolated_magnitudes[frame], 
                                levels=50, cmap='viridis', vmin=vmin, vmax=vmax)
            ax.contour(self.grid_x, self.grid_y, interpolated_magnitudes[frame], 
                    levels=20, colors='black', alpha=0.3, linewidths=0.5)
            
            time_text.set_text(f'Time: {frame * self.dt:.2e} s')
            return [time_text]
        
        anim = animation.FuncAnimation(fig, animate, frames=len(self.data),
                                    interval=200, blit=False, repeat=True)
        
        # Save animation
        print(f"Saving animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=5, dpi=150)
        plt.tight_layout()
        
        return anim

if __name__ == "__main__":
    animator = VTUAnimator(data_dir="./data", dt=1e-12)
    animator.load_data()

    # Smooth interpolation already uses griddata
    animator.create_smooth_magnitude_animation("smooth_velocity_magnitude.gif")