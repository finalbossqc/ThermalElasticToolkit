import meshio as mio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import Normalize
from scipy.interpolate import griddata, LinearNDInterpolator
from scipy.spatial import Delaunay
import os
from mpl_toolkits.mplot3d import Axes3D
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
        """Load VTU files and extract mesh data"""
        # Get list of VTU files
        os.system(f"ls {self.data_dir} | grep _0.vtu > ./frames")
        
        with open("./frames", "r") as f:
            frames = [line.strip() for line in f.readlines()]
        
        # Sort frames numerically if they have numeric prefixes
        try:
            frames.sort(key=lambda x: int(x.split('_')[0]))
        except:
            frames.sort()
        
        print(f"Found {len(frames)} frames")
        
        # Load meshes
        for i, frame in enumerate(frames):
            filename = os.path.join(self.data_dir, frame)
            try:
                mesh = mio.read(filename)
                self.meshes.append(mesh)
                if i == 0:
                    self.points = mesh.points
                print(f"Loaded frame {i+1}/{len(frames)}: {frame}")
            except Exception as e:
                print(f"Error loading {frame}: {e}")
        
        # Extract data arrays
        self.data = []
        for mesh in self.meshes:
            self.data.append(mesh.point_data)
        
        self.data = np.array(self.data)
        print(f"Data shape: {self.data.shape}")
        
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
                                        grid_resolution=150):
        """Create smooth animation of velocity magnitude using interpolation"""
        if self.data is None:
            self.load_data()
        
        self.setup_interpolation_grid(grid_resolution)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Calculate velocity magnitude for all frames and interpolate
        print("Interpolating velocity magnitude data...")
        interpolated_magnitudes = []
        
        for i, frame_data in enumerate(self.data):
            u = frame_data['u']
            v = frame_data['v'] 
            w = frame_data['w']
            magnitude = np.sqrt(u**2 + v**2 + w**2)
            
            # Interpolate magnitude onto regular grid
            interp_magnitude = self.interpolate_data_2d(magnitude)
            interpolated_magnitudes.append(interp_magnitude)
            
            if i % 10 == 0:
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
        
        # Overlay original mesh points
        scatter = ax.scatter(self.points[:, 0], self.points[:, 1], 
                           c='white', s=10, alpha=0.7, linewidth=0.5)
        
        # Formatting
        ax.set_xlabel('X coordinate', fontsize=12)
        ax.set_ylabel('Y coordinate', fontsize=12)
        ax.set_title('Smooth Velocity Magnitude Evolution', fontsize=14)
        ax.set_aspect('equal')
        
        # Time text
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, 
                           fontsize=12, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        def animate(frame):
            # Clear previous contours
            for coll in ax.collections:
                if coll != scatter:
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
        anim.save(save_path, writer='pillow', fps=25, dpi=150)
        plt.tight_layout()
        
        return anim

    def create_interpolated_contour_animation(self, save_path="velocity_tri_contour.gif"):
        """Contour animation using linear shape functions over mesh triangles"""
        if self.data is None:
            self.load_data()
        
        fig, ax = plt.subplots(figsize=(10, 8))

        # Create triangulation object once from mesh
        tri = mtri.Triangulation(self.points[:, 0], self.points[:, 1])

        # Compute velocity magnitudes
        magnitudes = []
        for frame_data in self.data:
            u, v, w = frame_data['u'], frame_data['v'], frame_data['w']
            mag = np.sqrt(u**2 + v**2 + w**2)
            magnitudes.append(mag)
        magnitudes = np.array(magnitudes)

        vmin = np.min(magnitudes)
        vmax = np.max(magnitudes)
        contour = ax.tricontourf(tri, magnitudes[0], levels=50, cmap='viridis', vmin=vmin, vmax=vmax)
        time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12,
                            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        def animate(frame):
            ax.clear()
            ax.set_aspect('equal')
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_title('Interpolated Velocity Magnitude (Triangulated FEM)')
            time_text = ax.text(0.02, 0.98, f'Time: {frame * self.dt:.2e} s',
                                transform=ax.transAxes, fontsize=12,
                                verticalalignment='top',
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            ax.tricontourf(tri, magnitudes[frame], levels=50, cmap='inferno', vmin=vmin, vmax=vmax)
            return []

        anim = animation.FuncAnimation(fig, animate, frames=len(magnitudes),
                                    interval=200, blit=False)
        print(f"Saving 2D triangulated contour animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=25, dpi=150)
        return anim

    def create_3d_interpolated_slice_animation(self, save_path="velocity_3d_slice.gif", z_slice=None):
        """3D interpolated slice animation using shape functions over tetrahedral mesh"""
        if self.data is None:
            self.load_data()
        self.setup_interpolation_grid()

        if z_slice is None:
            z_slice = np.median(self.points[:, 2])

        fig, ax = plt.subplots(figsize=(10, 8))

        interpolated_slices = []
        for frame_data in self.data:
            u, v, w = frame_data['u'], frame_data['v'], frame_data['w']
            mag = np.sqrt(u**2 + v**2 + w**2)

            # Linear shape function interpolation in 3D using tetrahedra
            interpolator = LinearNDInterpolator(self.points, mag, fill_value=0.0)
            query_points = np.column_stack([
                self.grid_x.ravel(),
                self.grid_y.ravel(),
                np.full(self.grid_x.size, z_slice)
            ])
            interp_mag = interpolator(query_points).reshape(self.grid_x.shape)
            interpolated_slices.append(interp_mag)

        interpolated_slices = np.array(interpolated_slices)
        vmin, vmax = np.min(interpolated_slices), np.max(interpolated_slices)

        def animate(frame):
            ax.clear()
            ax.set_aspect('equal')
            ax.set_title(f"Velocity Magnitude Slice at z={z_slice:.2f} — Time {frame * self.dt:.2e} s")
            cf = ax.contourf(self.grid_x, self.grid_y, interpolated_slices[frame],
                            levels=50, cmap='plasma', vmin=vmin, vmax=vmax)
            return []

        anim = animation.FuncAnimation(fig, animate, frames=len(interpolated_slices),
                                    interval=200, blit=False)
        print(f"Saving 3D slice animation to {save_path}...")
        anim.save(save_path, writer='pillow', fps=25, dpi=150)
        return anim

    def print_data_summary(self):
        """Print summary statistics of the data"""
        if self.data is None:
            self.load_data()
        
        print("\n" + "="*50)
        print("DATA SUMMARY")
        print("="*50)
        print(f"Number of frames: {len(self.data)}")
        print(f"Number of points: {len(self.points)}")
        print(f"Time step: {self.dt:.2e} s")
        print(f"Total time: {(len(self.data)-1) * self.dt:.2e} s")
        
        # Statistics for each component
        for comp in ['u', 'v', 'w']:
            comp_data = [frame_data[comp] for frame_data in self.data]
            comp_array = np.array(comp_data)
            
            print(f"\n{comp.upper()} component:")
            print(f"  Range: [{np.min(comp_array):.2e}, {np.max(comp_array):.2e}]")
            print(f"  Mean: {np.mean(comp_array):.2e}")
            print(f"  Std: {np.std(comp_array):.2e}")
        
        # Velocity magnitude statistics
        vel_magnitudes = []
        for frame_data in self.data:
            u = frame_data['u']
            v = frame_data['v'] 
            w = frame_data['w']
            magnitude = np.sqrt(u**2 + v**2 + w**2)
            vel_magnitudes.append(magnitude)
        
        vel_magnitudes = np.array(vel_magnitudes)
        print(f"\nVelocity Magnitude:")
        print(f"  Range: [{np.min(vel_magnitudes):.2e}, {np.max(vel_magnitudes):.2e}]")
        print(f"  Mean: {np.mean(vel_magnitudes):.2e}")
        print(f"  Std: {np.std(vel_magnitudes):.2e}")

if __name__ == "__main__":
    animator = VTUAnimator(data_dir="./data", dt=1e-12)
    animator.load_data()
    animator.print_data_summary()

    # Smooth interpolation already uses griddata
    animator.create_smooth_magnitude_animation("smooth_velocity_magnitude.gif")

    # New 2D triangulated FEM-style contour animation
    animator.create_interpolated_contour_animation("velocity_tri_contour.gif")

    # New 3D slice interpolation using tetrahedral mesh
    animator.create_3d_interpolated_slice_animation("velocity_3d_slice.gif", z_slice=0.0)